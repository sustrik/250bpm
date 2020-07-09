# Code Generation & Visual Smog in Code (part I)



### 1.

I am reading that code generation — then called "automatic programming" — originally referred to the automation of the task of punching the paper tape. Later on it became to mean generation of the real code from a higher level language like, say, Fortran.

Today it's not longer about creating full-blown programming languages. It's still about compilers, but rather about compilers for ad hoc, domain-specific and thow-away languages.

### 2.

Technically, to implement a compiler one needs two major parts: First, a general-purpose language to write the compiler in. Second, a parser.

Traditionally, compilers are implemented using C as an implementation language and tools like [yacc](https://en.wikipedia.org/wiki/Yacc) to do the parsing part. However, if you need to write a throw-away compiler in two minutes, none of those fares particularly well. Both C and yacc are hard, time-consuming and error-prone to use.

Instead, you want a powerful, easy to use scripting language with an extensive set of libraries, something like Perl, Python or Ruby.

As for the parsing, you don't want to create a new language from scratch. Two minutes is not enough time to do that. Instead, you want a well-known shrinkwrapped language that allows for creating arbitrarily complex structures, while making no assumptions about the semantics. In short, we want JSON, YAML or XML.

### 3.

Given that both the implementation languages and the parsers and widely-available, free and easy to use, writing a code generator is a technically trivial task.

So, is there any need for a specialised tool for code generation in the end? Why not simply parse an XML file from Python?

And the answer is: Because readability.

Source code of code generator is notoriously ugly and hard to comprehend. And the code that cannot be read, cannot be maintained, fixed or shared with others. Any code generation tool should thus put the main focus on readability.

### 4.

Me being a C programmer, let's have a look at C example:

    printf ("Hello, world!\n");

Now let's write code that will generate the code above:

    printf ("printf (\"Hello, world!\\n\");");

And code that will generate the above generator:

    printf ("printf (\"printf (\\\"Hello, world!\\\\n\\\");\");");

Yuck!

### 5.

Let me introduce a new term here: By "visual smog" I mean graphical elements in the code that are needed from syntactical point of view, but which don't contribute in any way to expressing the programmer's intent.

    printf ("printf (\"printf (\\\"Hello, world!\\\\n\\\");\");");

The intent of the above code is "_generate a program that will generate a program that will print a string to stdout_". However, around 50% of the code is not helpful in coveying the message and rather gets into the way. The amount of visual smog in the example is extremely high.

### 6.

As far as I can say, visual smog in code generators emanates from three major sources:

1.  Repetitive code
2.  Escape sequences
3.  Inconsistent indentation

### 7.

Code like the one below contains a lot od visual smog:

    printf ("#include <stdio.h>\n");
    printf ("\n");
    printf ("int main () {\n");
    printf ("    printf ("Hello, world!\\n");\n");
    printf ("    return 0;\n");
    printf ("}\n");

Most of it is created by the repetitive printf statement. In past couple of weeks I've played with code generation and, in the process, I've written a simple code generation tool called [ribosome](https://github.com/sustrik/ribosome). There, I've decided to replace the leading print statement by a single typographically lightweight and easy-to-type character:

    .#include <stdio.h>
    .
    .int main () {
    .    printf ("Hello, world!");
    .    return 0;
    .}

### 8.

The control language in the case of ribosome is JavaScript and Ruby rather than C. I've discarded Perl for it's cryptic syntax — we are trying to improve the readability here, mind you! — and Python because its indenting rules clash with the requirements for a code generation tool. In the end, the mix of control language and generated language looks something like this:

    for i in 1..5
    .printf ("Hello, world!\n");
    end

Which, of course, generates the following code:

    printf ("Hello, world!\n");
    printf ("Hello, world!\n");
    printf ("Hello, world!\n");
    printf ("Hello, world!\n");
    printf ("Hello, world!\n");

To understand my comment about Python above, consider that the dot (.) must be the first character in the line. If it was possible to put the dot operator anywhere on the line, we would have to escape any other dot characters in the generated code:

        .System\.out\.println ("Hello, world!\n");

  
Assuming that that's not an option, let's imagine the hello world example above with Python as a control language:

    for i in range(1,5):
    .printf ("Hello, world!\n");

Given the Python's syntax, now we have to way to express whether the dot statement should be a part of the loop or whether it should be executed once after the loops ends.

By the way, [Mako](http://www.makotemplates.org/) code generator uses Python as the control language, but has to add extra syntactic costructs to the language:

    % for name in row:
        <td>${name}</td>\
    % endfor

### 9.

The next interesting question is: Why do we prepend the lines of output by dot rather than the lines of Ruby code? Why not the other way round? Or, for what it's worth, why not use two different prefix characters to distinguish between the two?

There are two answers. One of them is kind of trivial, the other one is more philosphical:

First: We know that dots at the beginning of the line are quite rare in Ruby. Even if dot happens to occur at the beginning of the line it should be easy to get rid of it by simply adding some whitespace. Thus, there's no much space for clashes, where a Ruby line would be accidentally mistaken for an output line. However, this reasoning doesn't work the other way round: We don't know anything about the language being generated. It may be C or Fortran or Lisp. It may be something completely different. We can't guarantee that there won't be dots at the beginnings of the lines.

In the worst case we would be generating a ribosome source file (meta-code-generation) which would mean a lot of dots at the beginnings of the lines. We would have to introduce escape sequences. And the least thing anyone wants in a code generator is more escape sequences.

Second reason: Most code generation tools use the paradigm of the "template". What it means is that you consider the source file to be a template that contains the destination code in almost the final form and the code generation tool is used only to replace few selected snippets in the file by generated values:

    #include <stdio.h>
    
    int main()
    {
        printf ("Hello, $(name)!\n");
    }

The template paradigm may work well for a simple function like _printf_ (and maybe it works OK for generating web pages), but once complex looping, branching and function invocation is added to the mix, the template doesn't look like a template anymore. It looks like what it really is, namely, a program that generates another program.

Thus, I believe, the user approaches the code generation tool with the intent of writing a code-generating code, not a template. And in ribosome I've done my best to accommodate that mindset.

What it means in practice is that user can start writing Ruby code straight away with no extra syntactic baggage. They can even copy existing Ruby code to a ribosome source file and expect it to work out of the box!

And that, of course, means that lines of Ruby cannot have any extra prefixes.

### 10.

As already mentioned, escape sequences are another ample source of visual smog. The only way to fully avoid escape sequnces is to use prefixes — which is exactly what ribosome does with the dot notation. The dot has special meaning ("pass the line to the output") only if it occurs as the first charcter in the line. The rest of the line can thus contain arbitrary characters, including dot, without a need for escape sequences:

    .System.out.println ("Hello, world!\n");

### 11.

Ribosome could have done with no escape sequences altogether, were it not for the need to embed ruby expressions into the generated code:

    name = "Alice"
    .printf ("Hello, @{name}!\n");

What I've tried to do with @{} notation (as well as with the three other remaining operators) was:

1.  Use two characters for the operator, not a single one.
2.  Choose an unlikely combination of characters, rather than a common one.

The very fact of using two characters as an operator lowers the chance of collision with the generated text quadratically. Using uncommon two-character sequences lowers the probabilty of collision to almost zero.

### 12.

There's one exception to the above reasoning: When generating ribosome source file by ribosome (meta-level) the character sequences representing ribosome operators won't be all that rare. Therefore, I've created a dedicated construct to deal with such meta-meta-meta issues.

Specifically, I've introduced a "nested expression of N-th level" operator. The idea is that the compilation of an expression of N-th level yields an expression of (N-1)-th level, until, in the end, compilation of 1st level nested expression yields the computed value of the expression:

    @3{x} => @2{x} => @{x} => x

For those who enjoy meta-programing, here's an practical example:

    .name = "Alice"
    ..Hello, @2{name}!

First compilation results in:

    name = "Alice"
    .Hello, @{name}!

And the second one yields:

    Hello, Alice!

### 13.

In the rare case where we need to generate @{ sequence without the result actually being an ribosome input file we must finally resort to a proper escape sequence. These are implemented as simple Ruby functions:

    .In the rare case where we need to generate @{at}{ sequence without...

**To be continued…**

**Martin Sústrik, April 21st, 2014**