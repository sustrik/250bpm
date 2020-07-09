# Where are Python macros?



Everyone believes that macros (as in C preprocessor and assembly macros) are the Bad Thing and no modern language with any self-respect has them.

Yes, UNIX philosophy explicitly says "Avoid hand-hacking; write programs to write programs when you can" but without a decent macro language, code generation has to be done by an external tool, which makes it obscure and unreadable for anyone beyond the author of the code. (We've actually seen this. OpenAMQ project was havily code generated which then prooved to be almost an inpenetrable barrier for the contributors.)

I think I know what happened: Everyone was scared away be the sheer ugliness and inadequateness of C preprocessor and nobody even tried to do the same thing again and better.

Here are some deficiencies of C macros system, just off the top of my head:

*   Why does it have non-C syntax?
*   Is it even Turing complete?
*   And even if it is, why the hell do I have to define 3 nested macros to do such a basic operation as string concatenation?
*   Why are such elementary primitives as \_\_COUNTER\_\_ not in the standard?

But it's too late to fix that.

What about newer languages though?

Perl: Nothing. Python: No macros. Ruby: Nada.

If you are thinking of implementing a new programming language that will take over the world, give humble old macros a chance. Just take care to implement it in a sane way. After all, macro is just a function that returns a string that then gets inserted into the source code.

**Martin Sústrik, July 5th, 2015**