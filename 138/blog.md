# Unikernels: No Longer an Academic Exercise

### Introduction

I've been following the [unikernel](https://en.wikipedia.org/wiki/Unikernel) area for years and I really liked the idea, but I was unconvinced about the possibility of the wide-scale adoption of the technology.

The cost was just too high. It required you to forget everything you knew, to drop all the existing code on the floor, to rewrite all your applcations and tools and start anew. (I am exaggerating, but not by much.) If [microkernels](https://en.wikipedia.org/wiki/Microkernel) never made it, the unikernels are not going to either.

Whatever the benefits, the cost was prohibitive.

### Unikernels as processes

Recent "Unikernels as Processes" paper by Koller, Lucina, Prakash and Williams ([free download](https://dl.acm.org/citation.cfm?id=3267845)) turns the situation on its head. It proposes to run unikernels as good old boring OS processes. The idea is that most of the stack that's currently in the kernel will be in libraries linked directly to the application. Only few calls would cross the user/kernel boundary.

![unikernel2.png](http://250bpm.wdfiles.com/local--files/blog:138/unikernel2.png)

### One-click security

Assuming that libraries implementing POSIX APIs are available (and they are; see e.g. [rumpkernel](http://rumpkernel.org/)) it should be possible to take your existing application and just recompile it as a unikernel. The application would work as it did before, but it would use only a few system calls.

So, on one hand, any vulnerability in the kernel outside of those few functions won't affect your application.

On the other hand, any vulnerability in, say, TCP or filesystem implementation would compromise your application — but the problem would be at the same time kept at bay by separation between OS processes (different address spaces etc.) It wouldn't result in compromising other applications running on the same machine.

Now think about that from economic point of view.

Vendors are finally forced to take security seriously. But all the options they face are rather unpalatable.

They can keep the status quo and pray that nobody bothers to hack them.

Or they have to fix security flaws which, likely, means security audit of the entire stack and then rewriting most of the legacy code. That's prohibitively expensive. Only few, if any, companies are able to afford that.

Unikernels-as-processes model is no panacea, it won't fix a SQL-injection vulnerability for you, but it addresses a broad class of highly dangerous security flaws (for estimates, see, for example, [this paper](http://ts.data61.csiro.au/publications/csiro_full_text/Biggs_LH_18.pdf)).

More importantly though, it's a once-click solution! It does improve security at close to zero cost.

That, in turn, gives business people an easy way out from this uncomfortable dead-end situation.

Based on the above, my guess is that the technology, once it is truly provides a one-click experience, will face a quick and widespread adoption.

### Portability

Compared to the one-click security, portability is just a minor selling point, but still:

As the moment, it's not trivial to port applications even between POSIX-compliant OSes, but porting to Windows is a pain in the ass, plain and simple.

Unikernels-as-processes model has an interface between the OS and the application consisting of a single digit number of functions. Once those few functions are available and work the same on all mainstream OSes an application written on one OS would just run on a different OS. (And I am not even mentioning the possibility of running it directly under the hypervisor or on bare metal.)

### Keep your tools

One of the things that hindered the adoption of unikernels was that they broke the existing tools and processes.

Typical question: If I am going to run my application as unikernel, how the hell am I going to debug it?

And while the debugger is the tool that comes to mind first the same problem applies for any tool that assumes that the application is a standard executable and that it runs as an standard OS process. That will likely break most build and deployment toolchains. It can break control interfaces, monitoring and who knows what.

With unikernels-as-processes it is no longer a problem. The application IS a standard executable. And it DOES run as a standard OS process. Only minor changes to tools and processes are needed.

In fact, the switch can even improve the tools. Consider debugging an application. Currently, you stop at the kernel boundary. There's no way to step into the implementation of, say, TCP protocol. If, on the other hand, TCP implementation is just a library linked into your application, then sure, step into it, place breakpoints inside it, do whatever you want.

### Next productivity boom

When open source infrastructure became widely adopted we have experienced a productivity boom. Instead of waiting for years until the commercial vendor implemented the feature you wanted, you could suddenly choose a free solution that aligned with your needs. And you could fix any broken or missing stuff yourself.

However, we've seen only a dampened-down version of this revolution in the operating systems space.

Sure, you can fork Linux kernel and implement the feature you need. But then you are faced with the dilemma of either maintaining the fork yourself or upstreaming the change to the mainline kernel.

In the former case, you are doomed to maintain the fork forever. That's annoying and costly. Moreover, you have to ask the users of your application to run your fork of the operating system. That's not going to make them happy. They'll imagine you going bankrupt next year and them having to maintain a custom fork of the kernel for the next decade. They will politely back down.

If, on the other hand, you choose to upstream the change, you'll have to fight Linus Torvalds to get your patch in. If he doesn't like it, you are out of luck and back to the previous option. Even if you manage to get the patch in, it'll take years till everyone updates their OS to include your feature. Do you have a customer running RHEL 5 with kernel from 2007? Oops! Not going to work! You will end up with time-to-market of 10 years and that's guaranteed to kill almost any business plan.

With unikernels-as-processes model, the problem disappears.

You want to tweak IP protocol implementation? Yeah, sure. Find an existing IP library on GitHub, patch it as needed and link it to your application. Done. Anyone can run it on their off-the-shelf OS.

**October 23th, 2018**