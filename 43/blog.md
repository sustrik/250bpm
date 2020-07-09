# Magic numbers in C



I was asked today why I often use magic numbers in my code.

It's a small issue, but I feel passionately about it as the current trend of replacing every constant by a symbolic name is extremely annoying. And insistence of some code analysis tools on treating all magic numbers as coding style errors drives me crazy.

Just the give you the context, here's an example of magic number:

    i = i + 4;

And here's a "fixed" version of the code:

    #define FOO 4
    ...
    i = i + FOO;

There are certainly cases where using symbolic names is good style. Two of them come immediately to mind:

First, the case where numeric value of the constant is irrelevant. The number is just a placeholder for a symbolic name:

    #define STATE_START 1
    #define STATE_ACTIVE 2
    #define STATE_SHUTTING_DOWN 3
    #define STATE_DONE 4

This is basically the use case for C enums or Ruby symbols (":foo" and such).

Second, the case where constant is used as a compile-time configuration parameter:

    #define BUFFER_SIZE 4096

The idea here is to define the value at a single point and then use the symbolic name elsewhere. That way, if need arises, we can change the value as needed by modifying a single line of code.

All that being said, what about other use cases? Cosider this code (you often encounter that kind of thing when parsing network protocols):

    uint8_t version = *((uint8_t*) ptr);
    ptr += 1;
    uint32_t seq = *((uint32_t*) ptr);
    ptr += 4;
    uint16_t id = *((uint16_t*) ptr);
    ptr += 2;

What about magic numbers beaing added to 'ptr' in the example? Should we rewrite it in the following way?

    #define VERSION_SIZE 1
    #define SEQ_SIZE 4
    #define ID_SIZE 2
    ...
    uint8_t version = *((uint8_t*) ptr);
    ptr += VERSION_SIZE;
    uint32_t seq = *((uint32_t*) ptr);
    ptr += SEQ_SIZE;
    uint16_t id = *((uint16_t*) ptr);
    ptr += ID_SIZE;

Does that make sense? Let's think about it.

Does it make the code more readable? Well, no. It actually makes it less readable. If you see a line like this:

    ptr += SEQ_SIZE;

You have to find the definition of SEQ\_SIZE at the different place in the file or even in a different file. Thus, smooth reading of the source code is interrupted by scrolling up and down, by grepping and so on.

So maybe the use of the symbolic constant makes the code more maintainable? Maybe you can adjust the behaviour of the program by simply changing a single line of code? Well, no.

This change:

    #define SEQ_SIZE 3

doesn't produce a modified program. It produces a broken program.

The value of SEQ\_SIZE is tightly bound to the program logic (namely to the fact that the field in question is of type uint32\_t) and cannot be changed at will.

You can still get rid of the magic number like this:

    ptr += sizeof (uint32_t);

But I would argue that it makes the code less readable when compared to simply using number "4" and I am not even speaking of extra effort you need to spend when typing the code.

As a conclusion: Don't treat magic numbers as bad coding style automatically. In some cases replacing magic numbers by symbolic constants makes the code pretty awful to read and maintain.

**Martin Sústrik, November 27th, 2014**