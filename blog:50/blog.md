# Finish your stuff



If there is one principle that should be added to the UNIX philosophy, it is:

"Finish your project."

It's the most simple, yet the most disregarded software engineering princinple I can think of.

I dare you to list three finished software projects.

Having hard time, eh?

Except for some basic UNIX tools, like grep or make, it's almost impossible to find anyting that's truly finished, not simply abandoned.

Imagine the carpenters were like programmers. You bought a chair. You bought it because you've inspected it and found out that it fulfills all your needs. Then, every other day, the carpenter turns up at your place and makes a modification to the chair. Some of the changes may be useful, some neutral, some are simply annoying and some, like those spikes protruding from the wood, make the chair no longer usable. But irrespective of that: You bought a damned chair and you want it to remain a chair, not to find out that it's some kind of protean piece of furniture that's a chair today and partly a table tomorrow and, who knows, maybe you'll be able to humidify your cigars in it next week. So you refuse to let the carpenter in just to find out next morning that the chair have sneaked out through the back door during the night and had nice shiny dental drill added. At this point there's no recourse but to burn the chair down, put its remanants into the cellar and pour some quality concrete over it to make sure it stays dead forever. But just before the movie ends, there's a shot showing a crack in the concrete making it clear that new, monstrous "Chair, version 2" sequel is coming. Soon.

In short, do finish your stuff.

Of course, it will need maintenance later on, bug fixes and security patches, but make it functionally complete in the first place.

Yes, I hear you claiming that your project is special and cannot be made functionally complete because, you know, circumstances X, Y and Z.

And here's the trick: If it can't be made functionally complete it's too big. You've tried to bite off a piece that's bigger than you can swallow. Just get back to the drawing board and split off a piece that can be made functionally complete. And that's the component you want to implement.

Here's my own experience:

First open source project I've worked on was [AMQP](https://www.amqp.org/) messaging protocol and its reference implementation. It was impossible to make it functionally complete because it was designed by committee and it kept growing all the time. If it still lives its long and tortured life it's probably able to sing and dance and provide light entertainment for the entire family by now.

Out of the frustration with AMQP I've started my own [ZeroMQ](http://zero.mq) project. No committee this time! Surely, I was able to make it functionally complete? Well, no. I've tried to make it do too much. It is a compatibility library, a async I/O framework, a message delimitation protocol and a library of messaging patterns. Today, almost eight years after its inception, the project is still under active development and heading towards the point where it will be able to [send email](http://www.catb.org/jargon/html/Z/Zawinskis-Law.html).

Next one: [nanomsg](http://nanomsg.org). An alternative to ZeroMQ. I've tried to limit the scope of project by splitting the transport functionality as well as messaging patterns into separate plug-ins. I was partially successful, but it is still too big a chunk to swallow in a single piece.

Lately, after 30 years in the programming business, I've finally managed to cut down my projects to a reasonable size.

[Ribosome](http://sustrik.github.io/ribosome/) is a code generator. It generates code and that's it. It's functionally complete. Since I wrote it I've fixed some bugs and it was translated to a couple of alternative programming languages (thanks to Apostolis Xekoukoulotakis and Ali Zaidi!). But that's it. No functionality was added. And, I assure you, there's no plan to do so in the future.

[Libmill](http://libmill.org) is a library that introduces Go-style concurrency to C. After couple of months of development it seems to functionally complete now. In the future it may be ported to different CPU architectures and opertating systems but there will be no functionality change. There will be bugfixes but no feature creep.

So, it seems, I am finally there.

Please join me in my effort and do finish your projects. Your users will love you for that.

**June 9th, 2015**