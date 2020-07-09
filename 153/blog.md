# Hull: An alternative to shell that I'll never have time to implement

Here's an idea. It's kind of crazy but it's also fun to think about.

Imagine a language which has every piece of its state stored in the filesystem.

Yes, I know it sounds weird but do read on!

### Datatypes

Let's say we do this:

    a = 1

What will happen under the covers is that file "a" will be created that contains nothing but "1".

Lists could be represented as files where each line corresponds to an item.

    b = [1, 2, 3]

The above would simply create file "b" with the following content:

    1
    2
    3

Filesystem also provides hash tables out of the box. They are called directories.

    c = {
      foo: 1,
      bar: {
        quux: 3
      }
    }

Which would create a directory "c" with file "foo" (containing "1") and directory "bar" containing file "quux" which would in turn contain "2".

Fun idea: For map indexing use operator / instead of \[\]. So, to access "quux" you would write "c/bar/quux" which happens to be the path to the file in question.

### Call stack

Of course, state of the program is not just about variables. We would have to represent the call stack in some way.

Easy to do! For each stack frame create a directory called "nextframe". The call stack would then look like a sequence of embedded directories:

    main
    |-- a # contains 1
    |-- b # contains 1\n2\n3
    `-- nextframe
        |-- c
        |   |-- foo # contains 1
        |   `-- bar
        |       `-- quux  # contains 2
        `-- nextframe
            `-- a # contains 2

In such a model, scoping is easy. If you want to access "b" in the innermost frame, just walk up the directory tree until you find a file (or directory) named "b".

Also, overrides work as expected. If you ask for "a" in the innermost frame, you'll get "2", not "1".

### Instruction pointer

Now you are probably wondering how would one persist the instruction pointer. The language needs to know which command is the next to execute after all and not making this information persistent defeats the entire point of the language.

Let's make it work this way:

When program is started, a copy of the source file is created. We'll call it a "todo" file.

Then the first line of the "todo" file is executed. Then it is removed from the file.

We'll do the same with the second and every subsequent line.

That way the "todo" file always contains a list of commands that are yet to be executed.

But hey, you cry, if there's a loop in the source code we can't just delete a command within the loop! We will still need it in the next iteration!

Easy to fix! Let's make each iteration of the loop create a new stack frame (we would want that anyway, to get proper variable scoping). The body of the loop would be then copied to the "todo" file of the new frame and executed. Once there's nothing left in the inner "todo" file the scope would be exited, the stack frame deleted and the parent could start new iteration of the loop with a new copy of the loop body. Finally, when there's no more iterations to do the parent will delete the entire loop construct, including the loop body and move on.

Let's have a look at an example:

    b = [1, 2, 3]
    for i in b:
      echo i

Once the first line is executed we end up with the following state on the disk:

    main
    |-- b # contains "1\n2\n3"
    `-- todo # contains "for i in b:\n  echo i"

First iteration of the loop is started. Interpreter creates a new stack frame and populated both the "i" variable and the local "todo" file:

    main
    |-- b # contains "1\n2\n3"
    |-- todo # contains "for i in b:\n  echo i"
    `-- nextframe
        |-- i # contains "1"
        `-- todo #contains "echo i"

Now the echo command can be executed which will print "1" and remove the statement from the "todo" file:

    main
    |-- b # contains "1\n2\n3"
    |-- todo # contains "for i in b:\n  echo i"
    `-- nextframe
        |-- i # contains "1"
        `-- todo #contains ""

"todo" file is empty now so we can exit and delete the scope:

    main
    |-- b # contains "2\n3"
    `-- todo # contains "for i in b:\n  echo i"

Note how the "for" construct deleted the first element of "b". This may or may not be a good idea, but it's simple, so let's go with it for now.

At this point we can do the entire dance described above for element "2", then for element "3".

Finally, there are no more elements in "b" and "for" construct is considered done. It can be deleted from the "todo" file.

    main
    |-- b # contains ""
    `-- todo # contains ""

As there's nothing more to do, the entire program can now exit.

### Why the hell?

I mean, it's a fun exercise, but why would anyone want to use such a language?

But once you start playing with concept a little you'll find out that it has some interesting properties.

### Debugging

For starters, it kind of feels like being in a debugger although there's no debugger anywhere in sight.

It's entirely possible to execute just one statement at a time. The entire state of the program is on the disk, so once you've executed one command you can execute the next one and so on.

In the process you can inspect all the variables: Remember? They are just files in the filesystem.

    $ hull next
    done: b = [1, 2, 3]
    $ cat b
    1
    2
    3

### Time travel

Given that the entire state of the program resides in a directory, you can backup the directory and proceed with the debugging. Then, when you want to return to the previous point, you just restore it from the backup and you are set to go.

### Laziness

Once again: Given that the entire state of the program is stored on the disk, it means that you can execute it partially, then do something else, then resume the execution.

For example, a parent program may be interested only in the first line of your program's output. It can run the interpreter until the first line is produced, then suspend it and go on with it's own stuff. When it needs the second line it would just resume your program and so on.

In this way it works very much like python generators. Or, for that matter, like unix pipes.

And it's also a bit like Haskell: No code has to be executed unless you actually need the results.

### Concurrency

Given that programs are interruptible, you can launch many of them and then schedule them as you wish. The scheduling can be driven by commands such as "give me the next line of output".

To put it in a different way: Forking is easy. Just copy the directory and run second instance of the interpreter.

Here we are getting into the area of CSP, goroutines and channels.

### Remote execution

Want to move the program to a different machine?

Easy! Just scp the directory to the machine in question. Then ask the interpreter to resume the execution where it has ended.

**April 28th, 2019**

EDIT May 4th 2019: Typesystem based on file extensions, including polymorphism: frobnicate(foo.json) can have different implementation than frobnicate(foo.xml)