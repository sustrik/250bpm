# Confessions of an Abstraction Hater

I've written about the [cost of abstraction](http://250bpm.com/blog:86) before. Once you are in the IT industry for couple of decades and once you've read couple of millions lines on legacy code you become healthily suspicious of any kind of abstraction. Not that we can do without abstraction. We need it to be able to write code at all. However, each time you encounter an abstraction in the code that could have been avoided you get a little bit sadder. And some codebases are sadder than Romeo and Juliet and King Lear combined.

Remember reading an unfamiliar codebase the last time? Remember how you've thought that the authors were a bunch of incompetent idiots?

People may argue that this is because legacy stuff is necessarily convoluted, but hey, at that point you were just skimming through the codebase and you weren't understanding it deep enough to tell your typical enterprise legacy monstrosity from a work of an architectural genius. The reason you were annoyed was because you were overwhelmed by the sheer amount of unfamiliar abstraction. (To prove that, consider what was your opinion of the codebase was few months later, after getting familiar with it. It looked much better, no?)

Keep that feeling in mind. Think of it when writing new code. How will a person who doesn't know first thing about this codebase feel when reading it?

The options are not palatable. Either you try to be clever, use abstraction a lot and they'll think you are a moron. Or you get rid of all unnecessary abstraction. You'll make their life much less frustrating but they'll think you are some kind of simpleton. (And they'll probably refactor the code to make it look more clever.)

I want to give a very basic example of the phenomenon.

Imagine that the requirements are that your program does A, B, C, D and E, in that order.

You can do it in the dumbest possible way:

    void main() {
        // Do A.
        ...
        // Do B.
        ...
        // Do C.
        ...
        // Do D.
        ...
        // Do E.
        ...
    }

Or maybe you notice that B, C and D are kind of related and comprise a logical unit of work:

    void foo() {
        // Do B.
        ...
        // Do C.
        ...
        // Do D.
        ...
    }
    
    void main() {
        // Do A.
        ...
        foo();
        // Do E.
        ...
    }

But C would probably be better off as a stand-alone function. You can imagine a case where somewhene would like to call it from elsewhere:

    void bar() {
        // Do C.
        ...
    }
    
    void foo() {
        // Do B.
        ...
        bar();
        // Do D.
        ...
    }
    
    void main() {
        // Do A.
        ...
        foo();
        // Do E.
        ...
    }

Now think of it from the point of view of casual reader, someone who's just skimming through the code.

When they look at the first version of the code they may thing the author was a simpleton, but they can read it with ease. It looks like a story. You can read it as if it were a novel. There's nothing confusing there. The parts come in the correct order:

    A
    B
    C
    D
    E

But when skimming through the refactored code that's no longer the case. What you see is:

    C
    B
    D
    A
    E

It's much harder to get the grip of what's going on there but at least they'll appreciate author's cleverness.

Or maybe they won't.

**January 27th, 2019**