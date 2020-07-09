# In the Defense of Spaghetti Code



Have you ever seen a function that spans 1500 lines of code?

At that point every semi-decent programmer curses spaghetti code in general and the author of the function in particular and embarks on the task of breaking it into managable chunks, trying to decompose the problem into orthogonal issues, layer the design properly, move the common functionality into base classes, create convenient and sufficiently generic extension points et c.

If done properly, they'll end up with well-defined components, short functions that do one thing only, and generally, with a nicer and more maintainable code.

Everybody is happy and everybody pats the semi-decent programmer on the back.

…

It turns out that the 1500-line function was parsing a network protocol. It is a 30-year old, complex and convoluted Behemoth of a protocol, defined by many parties fighting over the specification, full of compromises and special cases, dragged through multiple standardisation bodies and then anyway slightly customised by each vendor.

At some point, the product is sold to a different customer who happens to need integration with a software from a different vendor, Foosoft Inc. As already said, there are minor differences in the protocol among the vendors. The parser has to be slightly altered.

Unfortunately, it turns out that the tweak intersects the boundary between two well-defined components in the implementation. The right thing to do would be to re-think the architecture of the parser and to re-factor the codebase accordingly.

However, the discrepancy in the protocol is really a minor one and has to accounted for by tomorrow. No way the programmer is going to sell the idea of re-factoring the whole parser to the management. Thus, he goes for the minimal change and modifies the following function:

    int new_sequence_number (int old_sqn)
    {
        return old_sqn + 1;
    }

in the following way:

    int new_sequence_number (int old_sqn, int foosoft)
    {
        if (foosoft)
            return old_sqn + 2;
        else
            return old_sqn + 1;
    }

Later on it turns out that the problem of non-consistent sequence numbering was recognised by yet another standards body (Bar Consortium) which released version 5.34.2 of the protocol that actually unifies the algorithm of generating the sequence numbers. Now we have to support version 5.34.2 as well:

    int new_sequence_number (int old_sqn, int foosoft)
    {
        if (foosoft == 2) // version 5.34.2 of the protocol
            return old_sqn + 3;
        else if (foosoft)
            return old_sqn + 2;
        else
            return old_sqn + 1;
    }

At this point you should be able to see where I am heading: After few such iterations the code that was originally nice and manageable becomes a mess of short functions plagued by lots of behavior-modifying arguments, the clean boundaries between components and layers are slowly dissolved and nobody is sure anymore what effect any particular change may have.

Let's imagine we want to make the above function nicer:

    int new_sequence_number (int old_sqn, int step)
    {
        return old_sqn + 1 + step;
    }

It looks all right but then it turns out that foosoft=4 is already being used to identify yet another vendor who uses sequence numbering step of 2. The beautification have actually broken the product! The patch is hastily reverted.

At this point everybody wishes they had only a single 1500-line long parsing function that would be much easier to understand, debug and modify than this mess of dozens of interconnected abominations. It's too late though to do that. Nobody dares anymore.

…

The point I am trying to make in this article is that sometimes it's the problem domain itself that's complex and convoluted. In short, it's a spaghetti domain.

Human-crafted and gradually evolved domains are often like this. Think of law. There are more exceptions than there are laws. Think of all kinds of standards. Regulatory directives. Products offered by a big bank. Different tastes os ARM microarchitecture.

In such cases you should seriously consider whether not even trying to break up the problem into fine-grained orthogonal chunks isn't the right thing to do. You may end up with long functions that will be frowned upon as spaghetti code by everyone who ever looks at the code, but you will sleep peacefully, knowing what kind of manageability nightmare you have avoided.

PS. If you happen to be a developer of a static analysis tool: Consider leaving long functions alone, rather then reporting them as suspicious. There are circumstances where long functions are perfectly legal and desirable.

EDIT: Long functions with gotos are as bad a mess of little functions. Luckily though, 45 years after Dijkstra's paper, goto is not used extensively any more.

EDIT: The discussion about this article on Reddit gave me an idea of good example of a spaghetti domain: Imagine you are modelling buildings in software. First you model [Empire States Building](https://encrypted.google.com/search?tbm=isch&q=empire%20states%20building&tbs=imgo:1). It's rectangular, it has 103 stories, most of them almost identical. Individual features are repeated over and over. etc. It's a nice example of orderly domain. It can be described in few simple functions. Then you try to model [Kowloon Walled City](https://encrypted.google.com/search?tbm=isch&q=kowloon%20walled%20city&tbs=imgo:1). Any possible generic rule you try to make about it was violated by some poor chinese emmigrant trying to survive in the compound. No feature is repeated. Ever. In such case it's better to draw a map (as the japanese speleological team that explored the building did) and put every little detail in there.

**March 25th, 2013**