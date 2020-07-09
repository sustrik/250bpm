# Getting rid of state machines (II)



So, as explained in the previous article, with green threads every state machine can be rephrased as a simple imperative function.

Nice. So we are done, aren't we?

Well, kind of. It's useful to do a reality check though.

And it turns out that in the reality state machines have an unfortunate tendency to spontaneously emerge in the code that was never meant to be a state machine.

Here's an example in pseudo-Go (I am too lazy to try to compile it). This example gets events from two distinct sources, A and B and counts them:

    func count(chanA chan string, chanB chan string) {
       sumA := 0
       sumB := 0
       for {
          select {
          case <- chanA:
              sumA++
          case <- chanB:
              sumB++
          }
       }
    }

Now imagine that communication with A becomes more complex. Let's say that the message from A is composed from a header and a body which are sent to the channel as two separate messages:

    func count(chanA chan string, chanB chan string) {
       sumA := 0
       sumB := 0
       for {
          select {
          case <- chanA:
              <- chanA
              sumA++
          case <- chanB:
              sumB++
          }
       }
    }

I assume you already see a problem with that: Receiving the body may block for unlimited amount of time. While it is blocked, no messages from B can be processed.

And here's a fix:

    func count(chanA chan string, chanB chan string) {
       sumA := 0
       sumB := 0
       hasHeader boolean := false
       for {
          select {
          case <- chanA:
              if !hasHeader {
                  <- chanA
                  hasHeader = true
              }
              else {
                  sumA++
                  hasHeader = false
              }
          case <- chanB:
              sumB++
          }
       }
    }

Do you see the state machine? If has a single bit of state (hasHeader) and two steps. The code is slightly ugly but it takes only a little bit more complexity in interaction with A or B to morph it into something really, really hideous.

What we see here is one state machine expressed as a goroutine (entire 'count' function) and another, hand-written and barely visible state machine that receives pair of messages from A. The two are tightly interwoven which is what makes the code look bad.

And of course, there's an easy solution. Just rip out the implicit state machine and turn it into a separate goroutine:

    func messageParser(chanIn chan string, chanOut chan string) {
       for {
            <- chanIn
            <- chanIn
            chanOut <- "message"
       }
    }
    
    func count(chanA chan string, chanB chan string) {
       chanParser := make(chan string)
       go messageParser(chanA, chanParser)
       sumA := 0
       sumB := 0
       hasHeader boolean := false
       for {
          select {
          case <- chanParser:
              sumA++
          case <- chanB:
              sumB++
          }
       }
    }

It would be nice if this technique was completely generic. In other words, if meticulous effort to split any interwoven state into separate green threads would result in a code with no overt or hidden state machines.

Unfortunately, that's not the case.

Specifically, this technique doesn't work when canceling green threads. Imagine that one of the channels in the example is used to cancel the goroutine:

    func count(chanA chan string, chanB chan string) {
       sumA := 0
       for {
          select {
          case <- chanA:
              sumA++
          case <- chanB:
              return
          }
       }
    }

You can split handling of chanB into a separate goroutine, but that would mean that original goroutine will never get canceled! If you add cancellation mechanism to it, you are back to step one. Uh, oh.

Now I am going to make a strong claim based only on intuition, not on any theoretical insight. I believe it to be true but feel free to attack it (and don't forget to bring counterexamples with you):

"If a language has efficient green threads and built in support for cancellation, every program can be decomposed into set of simple functions containing no implicit or explicit state machines."

To be clear, the built in cancellation mechanism must support wide array of use cases:

1.  Cancel entire program leaving no resource leaks behind.
2.  Cancel a subsystem without any leaks.
3.  Cancel a subsystem when a timeout expires. No leaks.
4.  Give subsystem a grace period to finish its work before canceling it.
5.  Grace period should be omitted if the subsystem has no work to do anyway.
6.  Allow for interwoven cancellation when cancellation of a supersystem happens while cancellation of a subsystem is in progress.

If the cancellation mechanism is not this generic users would have to implement these use cases by hand which will in turn lead to introduction of state machines into the code.

I've been trying to design such a cancellation mechanism for several years and I have repeatedly failed. Finally, I believe I have a solution that may work. I am going to describe it in the next article.

**Martin Sústrik, January 25th, 2016**