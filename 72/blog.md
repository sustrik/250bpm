# Select Statement Considered Harmful



Abstract
--------

This article is a follow-up to Edgar Dijkstra's classic ["Go To Statement Considered Harmful"](http://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf) article. It takes Dijkstra's premise and applies it to concurrent programming.

Program and Process
-------------------

Dijkstra says:

> My second remark is that our intellectual powers are rather geared to master static relations and that our powers to visualize processes evolving it time are relatively poorly developed. For that reason we should do (as wise programmers aware of our limitations) our utmost to shorten the conceptual gap between the static program and the dynamic process, to make the correspondence between the program (spread out in text space) and the process (spread out in time) as trivial as possible.

My observation is that in the code using select, whether POSIX select() function, Go select{} statement or an equivalent in other languages, the correspondence between code layout and its execution is severely harmed.

Consider the following example (in Go):

    for {
      select {
      case <- channelA:
          doA()
      case <- channelB:
          doB()
      case <- channelC:
          doC()
      }
    }

The order of execution of individual clauses has no relationship whatsoever to their ordering in the code.

On the other hand, in the following snippet the ordering corresponds 1:1 to the execution order:

    <- channelA
    doA()
    <- channelB
    doB()
    <- channelC
    doC()

It gets worse when the execution requires to preserve some state between the steps:

    var varA int = 0
    var varB int = 0
    var varC int = 0
    for {
      select {
      case varA <- channelA:
          doA()
      case varB <- channelB:
          doB(varA)
      case varC <- channelC:
          doC(varB)
      }
    }

What happens if case B is executed before case A? And what happens if C is executed after A, but B is missing? We are facing exponential explosion of complexity.

The latter pattern, on the other hand, keeps complexity at bay:

    varA := <- channelA
    doA()
    varB := <- channelB
    doB(varA)
    varC := <- channelC
    doC(varB)

Ideally, if we want to preserve our ability to maintain the program and reason about it, we should strive to use the linear pattern and avoid the select-based pattern altogether.

The question is whether every select-based program can be converted into linear program. Or whether getting rid of select necessarily limits the expressiveness of the language.

Let's consider different use cases and see what can be done.

State Machines and Event Loops
------------------------------

First of all, select-based programming is used in C to write network servers. The idea is to have many TCP connections to clients opened in parallel, to wait for activity on any of them using select(), then to service whoever happens to ask us to do some work. Reader can readily come up with their own examples in different languages and different problem domains.

This pattern is called event-driven programming or state machine approach. An interesting observation is that state machines are one of couple cases where using goto statement still yields nicer code than using structured programming. This isn't at all accidental. What we are facing here is the half a century old Dijkstra's problem resurfacing in the concurrent environment.

If we dig deeper into the network server problem, it can be seen that we can get rid of the state machine approach by forking a separate process for each TCP connection. This is the canonical way to solve the problem in the UNIX tradition, which itself is not that much younger than the original 'considered harmful' paper.

The reason why people use select() nonetheless is simple: Forking a process per TCP connection is simply too expensive. A program that would do so won't be able to cope in modern high performance environment.

So, we are not facing a conceptual limitation, but rather a relatively simple performance issue. And most modern languages do offer a way to fork lightweight processes (called green threads, coroutines, goroutines and so on) that make the option of launching one per TCP connection a viable proposition once again.

Go and Timeouts
---------------

Interestingly, Go, the language that is closest to the original UNIX philosophy, encourages handling network connections this way, but is still features a select{} statement.

We'll explore the remaining use cases in the rest of the article but let's first do away with a trivial case of using select{} for timeouts:

    switch {
    case time.After(100):
        handleTimeout()
    case <- channelA:
        doA()
    }

It seems that timeouts are handled this way in Go because select{} statement was already available and thus the designers of the language took advantage of the mechanism to solve this relatively simple and benign problem. It definitely doesn't look like select{} was introduced to the language because of dire need to solve the menacing timeout problem.

In fact, timeouts can be solved by simply adding an additional parameter to blocking operations. Here's an example in idiomatic C:

    int rc = foo(1); /* timeout of 1 second */
    if(rc == -1 && errno == ETIMEDOUT)
        handle_timeout();

Two Big Use Cases
-----------------

That being said, we are left with the cases where select{} is used for parallel communication with different goroutines. These can be split into two big classes. First, there are use cases where we want to communicate with many instances of the same thing. For example, in a network server there may be a goroutine per TCP connection but all of those want to communicate with the main goroutine. Second, there are use cases we want to communicate with different things. For example, we have a random number generating goroutine, a TCP connection goroutine, a statistics gathering goroutine and so on. Main goroutine wants to speak with all of those.

Unlimited Number of Identical Peers
-----------------------------------

Let's first tackle the problem of "many of the same type". Naively, one could create a channel for each of those peers and then use select{} (or rather reflect.Select() which allows for unlimited number of peers) to wait for activity from any of them.

Luckily, Go language already contains a mechanism to deal with this scenario in a clean way. Specifically, single Go channel can be used by many senders and many receivers at the same time. Thus, it works as (de)multiplexing device and removes the need for (de)multiplexing via select{} statement:

    ch := make(chan int)
    go(worker(ch))
    go(worker(ch))
    go(worker(ch))
    result := <- ch // waits for a message from any of the 3 workers

One may object that this way we lose the information about which worker is the message coming from. But that's exactly the point. If we are dealing with arbitrary number of instances of the same type we positively don't want to handle each of them in a different way. If we do, they are probably not the same thing after all. For example, we may have a bunch of TCP connections but some of them are HTTP connections while others are SMTP connections. We want to handle them differently. I'll discuss that in the 'different peers' section below.

Before moving there though let's have a look at a slightly confusing scenario of different peers that we want to handle the same way. For example, our application may receive inputs via console, via email or via SMS. These look like different things, but given that any of them provides same kind of input they can be treated as 'multiple instances of the same thing' and connect to the main goroutine via a single channel:

    ch := make(chan int)
    go(consoleHandler(ch))
    go(emailHandler(ch))
    go(smsHandler(ch))
    result := <- ch // waits for a message from any of the 3 handlers

The lesson from this example is that word 'same' in the phrase 'many of the same kind' refers to identical semantics, not necessarily to identical implementation.

Limited Number of Different Peers
---------------------------------

Having dealt with the 'same thing' case, let's have a look at how to deal with communicating with different kinds of things.

    for {
      select {
      case <- channelA:
          doA()
      case <- channelB:
          doB()
      }
    }

Let's suppose that A and B are completely independent. There's no ordering relationship between doA's and doB's. They can be executed in any order. They don't pass any info each to the other.

In such case each of the handles can be placed into its own goroutine with no need for select{} statement:

    func handlerA(channelA chan int) {
        for {
            <- channelA
            doA()
        }
    }
    
    func handlerB(channelB chan int) {
        for {
            <- channelB
            doB()
        }
    }

Let's, on the other hand, assume that there is a relationship between A and B. For example, doA returns a value that is then passed to doB. If so the program can be rewritten in linear manner:

    for {
        <- channelA
        varA := doA
        <- channelB
        doB(varA)
    }

At this point I would like to claim that any program dealing with limited number of different peers can be transformed into an equivalent program with no select{} statements. It can be done by repeatedly applying the two transformations shown above:

1\. Splitting independent stuff into separate processes.  
2\. Linearisation of the dependent stuff.

TODO: Formal proof. (The raw idea is that if there are two operations, either one is dependent on the other in which case they can be linearised; or they are independent in which case they can be parallelised. Use induction to prove it for any number of operations.)

Closing Remarks
---------------

As a final remark let me note that 'limited number of identical peers' is a trivial case and 'unlimited number of different peers' is not realistic as it would require infinite amount of code.

It was also brought to my attention that doing RPC via channels may be a case where select{} statement is truly needed.

The argument goes like this: Imagine we have one server goroutine and many client goroutines. Client goroutines are sending requests to the server goroutine via a single channel as described above. Each message contains a reference to the reply channel. Server is supposed to process the request and send the result to the reply channel.

And the question is: What happens if the reply cannot be sent to the reply channel straight away? The send operation can't block as that would DoS the entire server. Surely we want to store the reply and select on the reply channel (along with the request channel) until is becomes writable?

Well, no. The channels can already be buffered (in Go, that is). Sufficiently large buffer should smooth out any peakiness in client performance. If the reply cannot be sent it means the buffer is full and thus that there's something wrong with the client. The correct behaviour is such case is shutting the client down and possibly logging the event.

RPC server should be thus implemented like this (unfortunately, the example is written in Go and has to use select{} statement to implement a timeout):

    for {
        request := <-requestChannel
        response := processRequest(request)
        select {
        case request.replyChannel <- response:
            continue
        otherwise:
            close(request.replyChannel)
            log.Error("Oh my God! Oh my God! Something bad happened!")
        }
    }

Conclusion
----------

If language contains following features:

1\. Lightweight processes.  
2\. Channels to communicate between them.  
3\. Many simultaneous senders per channel.  
4\. Many simultaneous receivers per channel.  
5\. Ability to make channels buffered.

Then there is no need for select statement.

**February 20th, 2016**