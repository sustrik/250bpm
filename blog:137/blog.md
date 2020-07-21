# Update on Structured Concurrency

Since I've written the article on [structured concurrency](http://250bpm.com/blog:71) and implemented [libdill](http://libdill.org/) the progress went on.

Most importantly, Nathaniel J. Smith has published his "[Notes on structured concurrency, or: Go statement considered harmful](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/)" article. (If you prefer to watch a video, go [here](https://www.youtube.com/watch?v=oLkfnc_UMcE).) It's better, more detailed and more eloquent than anything I have ever written on the topic. If you want to read one thing about structured concurrency go read Nathaniel's article.

After C-based libdill we've also got [Venice](http://zewo.github.io/Venice/) which brought structured concurrency to Swift and [Trio](https://trio.readthedocs.io/en/latest/) which brought it to Python.

Then, few weeks ago, a new version of Kotlin's coroutine library was released that supports structured concurrency. Here's the accompanying [blog post](https://medium.com/@elizarov/structured-concurrency-722d765aa952) by Roman Elizarov.

"[Concurrency made easy: coming soon to a programming language near you](https://medium.com/@belm0/concurrency-made-easy-d3fdb0382c58)" recently published by John Belmonte takes another thoughtful shot at explaining the paradigm. It also summarizes the state of its adoption.

Finally, I would like to point out Aleksey Kladov's blog post "[Exceptions vs Structured Concurrency](https://matklad.github.io/2018/06/18/exceptions-in-structured-concurrency.html)" which goes beyond simple "let's tie thread lifetimes to lexical scopes!" agenda and discusses some hard questions of the actual semantics implied by structured concurrency paradigm. He does so in the context of Rust's [crossbeam](https://github.com/crossbeam-rs/crossbeam) library. We need more stuff like this.

All of that is great work and I hope we'll see more of it in the future!

For now, let me make few comments about stuff that may not be new, but which is sort of advanced and haven't been covered well enough yet.

### Thread bundles: It's not just syntactic sugar

Libdill, Trio and Kotlin all introduce a concept of thread bundles. In libdill it's called "bundle", in Trio it's "nursery", in Kotlin it's "scope" (it would be nice to have some unified terminology here). At first sight it looks just like syntactic sugar that allows you to cancel all the threads within the bundle in one go.

However, it's more than that. It allows you to cancel a bunch of threads in **parallel**.

To understand why it matters, consider a network server with 1000 open connections. Each connection is handled by its dedicated thread. Also, let's assume we want to give each connection one second to do clean shutdown, to perform termination handshake with the peer etc.

If we canceled the connections in a simple for loop, the shutdown of the server would take, in the worst case, 1000 seconds, i.e. more than 16 minutes. In fact, if you are facing a DoS attack that opens connections and then leaves them hanging, it would take exactly 16 minutes 40 seconds. If, on the other hand, there was a construct to cancel the connections in parallel, the server would shut down in just one second. That's a difference that would make ops people cry.

### Ordered cancellation

There's a temptation to equate thread bundles with scopes: All the threads launched within the scope would be canceled in parallel when the scope is exited.

There's a problem with that. Imagine that, within the scope, we create a logging thread first, then wait for incoming connections and launch one thread per connection. Given that all the threads were launched within the same scope, they will be canceled in parallel. It may happen that the logging thread would exit first. In that case all the logs produced by the connections while they are shutting down would be lost.

What we really want is shutting down the connections first, then shutting down the logging thread.

You can do that by nesting the scopes like this:

    async with trio.open_nursery() as n1:
        n1.start_soon(logger)
        async with trio.open_nursery() as n2:
            while True:
                ...
                n2.start(connection)

Doable, but consider that instead of two threads you had five threads. And you wanted to cancel them in a particular order. The five nested blocks would look somewhat ugly.

One way to deal with that would be to adopt semantics a bit like that of C++ destructors: The destructors are called in the reverse order of how the constructors were called.

    {
        nursery n1;
        n1.start_soon(logger);
        nursery n2;
        while(1) {
            ...
            n2.start_soon(connection);
        }
    } // n2 is shut down here (all connections in parallel), when done, n1 is canceled

We should also think about whether it would be worth it — at least in statically typed languages — to impose a discipline on the programmer and allow them to run only one type of thread within one bundle/nursery. It would mean that different types of threads could not be shut down in parallel. But that's probably what we want anyway. (Counterexamples are welcome!)

    {
        nursery<logger> n1;
        n1.start_soon();
        nursery<connection> n2;
        while(1) {
            ...
            n2.start_soon();
        }
    }

### Deadlines, cancellations, grace periods

Imagine, again, the case of a network server. We may want to limit the lifetime of each connection to one hour. If it's lasts longer than that it either means that we've lost connectivity or that the peer is trying to perform a DoS attack. So let's just shut it down.

So far so good.

However, imagine we want to shut down the server. Canceling everything immediately would be easy. Just exit the main scope.

But we still want to give connections a one minute grace period to shut down cleanly. What we can do, in the main thread, is to sleep for one minute, then exit. But it feels ugly. Why wait for one minute even if all the connections terminated within few seconds?

We have a conflict of deadlines here. The connection threads are supposed to deadline in both one hour and one minute. How are we supposed to deal with that in a clean way?

Libdill provides bundle\_wait() function which has a deadline parameter. It waits for all the threads in the bundle (nursery) to finish. When they do, it exits. If the deadline expires and some threads are still running it cancels them and exits.

This approach works for C where cancellation has to be done by hand anyway, but it's kind of clumsy in more sophisticated languages where it is supposed to happen automatically.

To be frank, I am not sure whether this scenario can be implemented in Trio. [This section](https://trio.readthedocs.io/en/latest/reference-core.html?highlight=timeout#cancellation-semantics) of the docs discusses the cancellation semantics but I don't see any obvious match there. (Correct me if I'm wrong!) I am not sure about Kotlin's implementation either.

### Multi-core support

Finally, it should be said that all the implementations that I am aware of use coroutines and ignore OS threads. What that means is they can't use structured concurrency on more than one CPU core. At the same time there seems to be no inherent reason why OS threads or processes couldn't be made part of the structured concurrency world.

There may be technical reasons though.

I once implemented launching of OS process that was semantically equivalent to launching a coroutine in libdill, with cancellation and everything. You just had to use go\_process() instead of go(). Surprisingly, it worked.

But then I deleted it. And I haven't even tried with OS threads.

The reason was that implementation of threads in the C standard library (pthreads) is complex and fragile. It contains a lot of corner cases and poorly specified behavior. Once signals are added to the mix all bets are off. Even if you make it work on one operating system, there's no guarantee that you won't experience weird behavior on a different operating system.

And I really don't want to deal with that complexity. Libdill is a hobby project and I have only limited time to spend on it.

But, eventually, if structured concurrency is to take off, it will have to deal with OS threads and processes. It would need people with enough free time and enthusiasm to deal with the complexity and maybe also some political will to change standard libraries in such a way that they play well with structured concurrency.

**October 19th, 2018**