# Getting rid of state machines (I)



I've written about state machines [before](http:///www.250bpm.com/blog:25).

The message I was trying to convey was that using state machines is superior to relying on callbacks.

Which it is. Most definitely.

However, state machines have a bunch of problems of their own.

In this article I wan to discuss these problems in detail and propose what has to be done to replace state machines by standard linear code.

What's wrong?
-------------

Let's go straight to the problem: State machines are large and brittle.

Typically, there's no built-in support for state machines in your language and so you end up managing a large amount of boilerplate code. (In theory, you could generate the boilerplate, but code generation is super contributor-unfriendly and thus should better be avoided.)

What's worse, the code is complex and hard to reason about. It's extremely easy to get wrong.

In practice, the common traversal paths through the state machines are written and debugged early in the development cycle and what you are left with are bugs in rarely used paths dealing with stuff like timeouts, cancelations or errors. Interactions between different state machines multiply the complexity and what results are rarely seen, non-deterministic heisenbugs that take ages to reproduce and fix.

What is a state machine?
------------------------

To fix the problems with state machines we first have to have clear understanding of what state machine is and what it isn't.

To put it simply, state machine is a computation, an algorithm.

It is very similar to 'function' (also known as procedure, method or subroutine), but unlike function it splits the computation is multiple smaller steps. The added value of the splitting is that the state machine can be interrupted each time it processes one step and before it starts processing the next one.

But what's the point? Why would anyone want to execute a function, which is a perfectly sane and nicely encapsulated unit of computation, in several steps?

And here we are getting to the core of the problem: You want to split the function because it may take too long to finish — it can do a lot of work or maybe just idly wait for I/O — and in the meantime it blocks other stuff from being executed.

Typical use of state machines is to run a step of one state machine, then run a step from another one and so on. In short, state machine is a very lightweight thread that user can schedule by hand. It is a manual alternative to an OS process or an OS thread.

Why state machines?
-------------------

The obvious question thus is: Why state machines? Why not processes or threads?

And the obvious answer is: Performance.

When UNIX was still young, scheduling was supposed to be done by the OS on per-process basis. When implementing a network server, for example, you were supposed to fork a new instance of the process for each TCP connection and rely on the OS scheduler to switch between the processes.

I guess it made sense from performance point of view back then. All the stuff that makes process switching slow today haven't yet existed. Machines had single processor, there was no virtual addressing or memory caches. In such an environment process switching was closer to what we call green threads today.

Later on came threads. Threads are like processes, but operate in the same address space, so there's no need to switch the TLBs. Thus, cost of context switch is lower.

Finally, we've got green threads. These are typically implemented on the language level and avoid even more cost. The latest and most optimised version is Golang's goroutines. They are cooperatively scheduled, thus there is no cost associated with preemption. They have tiny stacks, maybe couple of kilobytes. They can even be scheduled on multiple CPU cores like real OS threads.

Goroutines are performance-wise comparable with hand-written state machines. It seems that there's no more space for radical performance improvement.

So, we can forget about state machines and use green threads instead, right?

Unfortunately no. Green threads, even if they bring us a long way towards the goal, aren't sufficient to eliminate all state machines. In next blog post I'll dig into the remaining problems in more detail.

**January 5th, 2016**