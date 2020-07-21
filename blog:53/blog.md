# A case for unstructured programming



Let me say few words about unstructured programming.

First of all, almost nobody can do it any more. You don't believe me? Just try writing you next project in unstructured way, Instead of:

    if(x) {
        do_stuff1();
        do_stuff2();
    }

write:

    if(!x) goto stuffed;
    do_stuff1();
    do_stuff2();
    stuffed:

Very soon you'll feel that creeping sense of insecurity: Am I doing it right? If this thing going to be maintainable? And what are the best practices anyway?

To be fair, the above doesn't apply to programmers who are fluent in assembly, but everyone else is encouraged to actually do this as an exercise. If nothing else, it will broaden your mind. For extra fun have a look at the [Duff's device](https://en.wikipedia.org/wiki/Duff%27s_device) before and after the exercise. What have seemed like a terrible hack before will turn into a reasonable solution, even to a thing of beauty.

Anyway, the real point I wanted to make today is that the programming languages called "structured" still have a lot of unstructured traits. And it's not because their authors sucked at programming language design and let the old, discredited constructs leak into modern languages, but because fully structured language is, for all practical purposes, unusable.

To be clear, structured language is a language where the control flow follows the syntactic structure of the code, where there are no random cross-jumps from one branch of the parse tree to another.

And yes, this time it's not the vilified goto who's the main culprit, but rather the humble and innocent 'return', along with 'break' and 'continue'.

Consider this program:

    while(1) {
        do_stuff1();
        if(condition())
            break;
        do_stuff2();
    }

And here's its fully structured counterpart:

    int done = 0;
    while(!done) {
        do_stuff1();
        if(condition())
            done = 1;
        if(!done) {
            do_stuff2();
        }
    }

And while the latter program may be only slightly ugly, trying to return from inside three nested loops in a structured way turns into an actual coding horror.

You may have already observed that the reason why unstructured traits aren't still showing any signs of demise from the modern programming languages is readability. Dijkstra argued that unstructured programming hurts readability (and thus maintainability) but now it turns out that even the structured way, if applied over-zealously, will do the same thing.

This argument looks like a straw man. In the end, nobody sane would write the fully structured program above. So what am I ranting about?

Well, it turns out that some programmers don't take full advantage of the unstructured traits in their language, resulting in some pretty ugly code:

    void foo(void) {
        if(condition1()) {
            do_stuff1();
        }
        else {
            if(condition2()) {
                do_stuff2();
            }
            else {
                if(condition3()) {
                    do_stuff3();
                }
                else {
                    do_stuff4();
                }
            }
        }
    }

Why not write it like this:

    void foo(void) {
        if(condition1()) {
            do_stuff1();
            return;
        }
        if(condition2()) {
            do_stuff2();
            return;
        }
        if(condition3()) {
            do_stuff3();
            return;
        }
        do_stuff4();
    }

It's good to understand why the latter example is more readable than the former one: It is not only a matter of the fact that large number of nested blocks tend to push the code out of the right side of the screen. More importantly, reading nested blocks means you have to maintain more context in your mind. If there are 5 nested blocks and you are reading the innermost one you are effectively keeping a 5-element parse stack in your mind, for the single purpose of being able to continue reading when you enconter the next 'else' statement.

Here's my advice: When creating a new nested block, spend a second considering whether the same thing cannot be achieved by simply by using 'return', 'break' or 'continue'. It may require moving some bits around but the resulting flat and readable code is definitely worth the hassle.

**July 18th, 2015**