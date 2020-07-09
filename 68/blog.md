# Enforced Error Handling



If you don't mind your program crashing once in a while — and I am not making fun here: for some programs making them 100% error proof doesn't pay off — using exceptions for error handling is pefectly adequate.

However, when writing code with strong reliability requirements your priorities are different. After all, large fraction of production outages comes from [botched error handling](http://danluu.com/postmortem-lessons/). You really want to stop and think about each error code at every level as it is passed up the stack. In that case C (or Go) style error handling is exactly what you want.

The problem with C (and Go) though is that it allows you to ignore the errors. It's perfectly all right not to check the error code or even not capture it in a variable. For example, this kind of thing is a common, almost a standard way to close a file descriptor:

    close(fd);

However, POSIX says:

    The close() function may fail if:
    [EIO] An I/O error occurred while reading from or writing to the file system.

Oops!

All that being said, I wonder whether there is an imperative language that enforces explicit handling of errors. For example like this:

    x = foo(y) err {
        // Handle the error here.
    }

In fact, you would still be able to ignore the error but you would have to make a conscious decision to do so:

    x = foo(y) err {}

Moreover, looking for ignored errors, which is really hard in C, given that there's no easy way to distinguish void function invocations from unchecked error codes, would become easy, both for human reviewers and for automated tools.

**December 19th, 2015**