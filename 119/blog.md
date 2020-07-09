# Documentation Driven Design

After spending full day adding new documentation to libdill and after getting desperate about the repetitivness of the man pages I've got rid of what I had and spent another day writing a program to generate the documentation.

Consider the use cases…

A lot of functions, for example, have deadlines. For each of those functions the man page should contain the following text:

> deadline: A point in time when the operation should time out, in milliseconds. Use the now function to get your current point in time. 0 means immediate timeout, i.e., perform the operation if possible or return without blocking if not. -1 means no deadline, i.e., the call will block forever if the operation cannot be performed.

A lot of functions are part of libdill's socket library. Those man pages should state that:

> This function is not available if libdill is compiled with —disable-sockets option.

A lot of functions have a "mem" variant (such as udp\_open vs. udp\_open\_mem) which have almost identical man pages, except for one added paragraph.

Almost all functions have the following piece of text about their return value:

> In case of error it returns XXX and sets errno to one of the values below.

All functions with deadlines can return ETIMEDOUT error and man pages shoudl say so.

All functions that can possibly use network can return ECONNRESET.

All functions related to a particular network protocol could share a single code example that should be copied into each man page.

And so on and so on.

So I wrote a program to generate all that and the input to that program is a JSON file, a list of all the metadata needed to generate the documentation.

What I've realized in the process was that it forced me think about consitency of libdill's API. If two functions were inconsistent in some way I had to add special case to my documentation generator. That in turn provides an incentive to fix the API and make it more consistent — an incentive that is often missing in the ordinary life of a programmer.

Furthermore, I've realized that by writing the metadata JSON file I have unwittingly created a formalized description of some aspects of the library that would, at first sight, seem to be too vague to be formalized. Let me give an example.

Imagine there is a subset of functions that only work if you pray to saint Isidore of Seville, patron saint of programmers. It's pretty hard to express that in a program. However, you still want a line in the man page saying:

> The function assumes that the user is praying to St. Isidore during its execution. It the condition is not met the function will exhibit undefined behaviour.

To be able to generate that line, each function in my JSON metadata file has a field saying "St-Isidore": true.

And it's not only St. Isidore who gets into the play here. Each function could also have metadata describing its dependencies, compile-time options, experimental status, performance characteristics, you name it.

And what's really nice about it is that I have an actual incentive to keep all those metadata in sync with reality, because otherwise my man pages would suck.

And that, of course, makes me wonder: What kind of new applications could we create if we had that kind of rich metadata available in machine-processable format?

**February 18th, 2018**