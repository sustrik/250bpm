# Kaizen of Programming



I've started programming early, in 1984 when I was 11 years old. Back then I just had an idea of what the program should do and I did whatever was necessary to get there.

After that initial period of pogramming I haven't cared about it too much. I did whatever programming assignments we've got in school and later whatever work I needed to do to feed myself, but that was it. In the spare time I was mostly drinking with artists.

That changed in 2004. Back then I started to be involved in open source. The fact that I was delivering code, not a packaged product, sparked my interest in programming again. You see, with packaged product you provide people with a tool to do stuff. That's super useful and a noble endeavour but, at least for me, it is not very interesting. Delivering code, on the other hand, means putting an idea into other peoples' minds. And that kind of thing has an aura of magic that's hard to resist.

50,000 LoC
----------

From 2007 to 2013 I've created [ZeroMQ](http://zeromq.org/intro:read-the-manual) and later [nanomsg](http://nanomsg.org/nanomsg). The idea I've tried to convey was that messaging patterns ([request/reply](https://raw.githubusercontent.com/nanomsg/nanomsg/master/rfc/sp-request-reply-01.txt), [publish/subscribe](https://raw.githubusercontent.com/nanomsg/nanomsg/master/rfc/sp-publish-subscribe-01.txt) etc.) aren't just some vague heuristics about how to make distributed systems but rather formally precise algorithms. Once you've understood what publish/subscribe means you knew exactly what kind of behaviour to expect from it and was able to use it as an atomic building block of your distributed application.

To pass that idea on I've created a library that encapsulated each of those patterns. As a user, you instantiated an publish/subscribe endpoint and that was it. It worked in publish/subscribe way. I hoped that people using the library will adopt those patterns and use them in their future work independent of whether they'll use ZeroMQ or not.

It took around 50,000 lines of code to get there.

5,000 LoC
---------

In 2015 I've created a library called [libmill](http://libmill.org/). It's an easy to use coroutine library for C. Most of the code there is just a legwork, trying to rewrite Go's model of concurrency and make it so fast that the speed of coroutine creation or a context switch would be comparable to simple control constructs like 'if' or 'for'. The idea is that concurrency is literally just a bunch of control constructs. And the hope was that having a library which makes them equal performance-wise would shift the peoples' mental model of them.

In 2016 I've forked libmill and created [libdill](http://libdill.org/). The new idea here was that of [structured concurrency](http://libdill.org/structured-concurrency.html). The idea that threads/coroutines can be cleanly nested in a similar way that we nest functions and objects. I've tried to examplify the concept by creating a [new socket API](https://github.com/sustrik/libdill/blob/master/rfc/bsd-socket-api-revamp.md) that allows for fine-grained layering of network protocols.

In this case we are speaking about approximately 5,000 lines of code.

76 LoC
------

In 2017 I've created a tool called [cartesian](https://github.com/sustrik/cartesian) to deal with problem domains that are both highly repetitive and at the same time somewhat irregular. The idea is that the model of subclassing that we know from object-oriented programming is not the only possible. Yes, we can categorize animals to 'mammals' and 'fish', but those same animals can be as well categorized to 'land animals' and 'water animals'. In the subclassing model we have to decide which of those distinctions is more important and go with that. In cartesian, on the other hand, you treat both distinctions equally, as [different dimensions of the same conceptual object](http://250bpm.com/blog:91).

The code to power it is very small. 76 lines of Javascript.

35 LoC
------

Last week I've written a small library called [tiles](https://github.com/sustrik/tiles). It comes from long experience with code generation. Your typical code generation product, like Jinja or Mako, or for that matter, my own Ribosome, are based on idea of a template code where you fill in some pieces dynamically. That makes sense if you want to generate a customized HTML page where all you want to change is say the username, the ID number and such. However once you try to generate an actual code, say a state machine, they become increasingly inconvenient. You have to mix the template code with the generator code which results in an unreadable mess.

Tiles, on the other hand, dispenses with the idea of the template and rather provides a way to manipulate and combine rectangular blocks of code in a simple fashion.

The module has 35 lines of code.

From Kaizen to Zen
------------------

You may have noticed a pattern. As the time goes by my code tends to be more and more concise. From 50,000 lines of code in 2009 to 35 lines of code in 2017.

One may consider that to be an improvement. As you get older and more experienced you can do more stuff with less code. What's there to object?

But let me ask a theoretical question: Is it possible to create a project with zero lines of code?

And yes, I can to imagine myself solving the last hurdle and finally deleting the last line of code. The project becomes perfect, yet, at the same time, incommunicable. Just try to imagine selling a library with zero lines of code. All that remains is mental pattern of how to solve the problem and there's no efficient way, short of telepathy, to instill that pattern into an other person's brain.

While it's totally reasonable for a person to use ZeroMQ (You don't want to write 50,000 lines of code yourself, do you?) why would they use Tiles, which is, after all, just a 35 lines long snippet of Python code?

But it's the act of using the library that establishes the idea behind it in your mind. If you don't use it you won't get the idea.

So, what appears to be an improvement in the terms of doing stuff, is actually a drawback in the terms of communicating an idea.

Kaizen, the process of continual improvement, have degraded to Zen, the act of solitary self-enlightment.

So here I sit, with no idea what to do.

**October 4th, 2017**