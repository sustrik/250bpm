# Tiles: Report on Programmatic Code Generation

Writing programs that generate programs is hard. The programmer has to think at two levels of abstraction at once. She has to follow the logic of the generator. At the same time she can't lose the focus on the logic of the generated code. And the two don't even have to be written in the same language!

That's a hard enough feat even when the tools aren't putting obstacles in your way. But, unfortunately, that's exactly what they are doing.

Consider this Python program that outputs the classic C "Hello, world!" program:

    def generate_hello(who):
        return """#include <stdio.h>
    
    main( ) {
            printf("hello, """ + who + "!\\n\");\n}"
    
    print(generate_hello("world"))

Ugly, you say? Yes, it's ugly. But it's just generating the simplest possible program! If we wanted to generate something truly complex it would become doubleplusugly.

But ugliness aside, the problem is that the code is unreadable.

Reading code is generally harder than writing code. Reading code with two parallel levels of abstraction is yet much harder. Add some atrocious formatting, sprinkle with copious amount of escape sequences and even the best programmer won't be able to understand what's going on.

The traditional solution to this problem is templating.

The idea is that the generated program is like a form, a pre-printed template with few blank slots to fill in:

![tiles1.gif](http://250bpm.wdfiles.com/local--files/blog:147/tiles1.gif)

And here's how it works with, say Jinja2:

    from jinja2 import Template
    
    t = Template("""#include <stdio.h>
    
    main( ) {
            printf("Hello, {{ who }}!\\n");
    }""")
    
    print(t.render(who="World"))

Well, it's not much better. Weird formatting and escape sequences remain. However, given that the template is now a single string we can load it from a file instead of using a string literal. The content of the file would look much better:

    #include <stdio.h>
    
    main( ) {
            printf("Hello, {{ who }}!\n");
    }

The downside is that the template and the generator now live in two different files which makes the logic harder to follow.

By the way, I am not picking on Jinja2 here. All the code generation tools I've looked at work in basically the same manner. Here's, for example, how Golang's text/template package looks like:

    package main
    
    import (
        "log"
        "os"
        "text/template"
    )
    
    func main() {
        // Define a template.
        const letter = `
    Dear {{.Name}},
    {{if .Attended}}
    It was a pleasure to see you at the wedding.
    {{- else}}
    It is a shame you couldn't make it to the wedding.
    {{- end}}
    {{with .Gift -}}
    Thank you for the lovely {{.}}.
    {{end}}
    Best wishes,
    Josie
    `
    
        // Prepare some data to insert into the template.
        type Recipient struct {
            Name, Gift string
            Attended   bool
        }
        var recipients = []Recipient{
            {"Aunt Mildred", "bone china tea set", true},
            {"Uncle John", "moleskin pants", false},
            {"Cousin Rodney", "", false},
        }
    
        // Create a new template and parse the letter into it.
        t := template.Must(template.New("letter").Parse(letter))
    
        // Execute the template for each recipient.
        for _, r := range recipients {
            err := t.Execute(os.Stdout, r)
            if err != nil {
                log.Println("executing template:", err)
            }
        }
    
    }

It code generation was really like filling in tax forms, the templating approach would be good enough.

But it's not.

Even the simple Go example above requires some extra logic. Specifically, it uses different text depending on whether the person is question attended the wedding or not.

But it gets worse.

Imagine you want to generate the following report:

    ACME Inc. - Payroll
        Alice $3000
        Bob $2500
        Carol $2800
        Dylan $2900
    Signature: .......... (Wile E. Coyote)

That's no longer filling in empty slots. The template has to loop through the list of employees and generate a line for each of them.

Again Jinja2:

    {{ company }} - Payroll
    {% for employee in employees %}
        {{ employee.name }} ${{ employee.salary }}
    {% endfor %}
    Signature: .......... ({{ director }})

As can be seen, moving to more complex generated text means adding more special constructs (if-then-else, for-in etc.) into the template until we end up with a full, Turing-complete code generation DSL.

There are two things I don't like about the templating approach to code generation:

First, I don't want to learn a new DSL. If I'm coding in Go, I want to use Go and I want to use its power fully. I don't want to use some crippled version of it that's used only inside of templates.

Second, I don't want to use large templates in the first place. The pieces I want to fill into the template are often too complex to be generated inside of the template and therefore I have to precompute them, put them in an array and then use text/template to render the array. That in turn tears the generation logic, which is a single conceptual thing, into two pieces: The precomputation and the template rendering.

And I am not even speaking of complex cases when I want to fill in a slot in a template not by a simple string but rather by a full template of its own.

Given the considerations above, I've created a [small Python library](https://github.com/sustrik/tiles) in 2017 to do code generation in a different way. The idea was to treat "a block of code" as a primitive type, not unlike string or integer. The user would then use the language — the real language, not a limited version thereof — to manipulate those blocks of code, add them together and eventually generate the entire program out of them.

    payroll = t/"@{company} - Payroll"
    for employee in employees
        payroll |= t/"@{employee.name} $@{employee.salary}"
    payroll |= t/"Signature: .......... (@{director})"
    print(payroll)

As can be seen, it's a pure Python. No template-specific DSL, no nothing. Instead, there's a new primitive type called "tile" that really just a rectangular area of text. Tile literals support tile interpolation (@{} stuff) but that's not much different from the existing Python string interpolation (F-strings) and can't be really claimed to be a separate language within a language. The user is free to manipulate the tiles in any way that she sees fit.

Unfortunately, since 2017, I haven't had a chance to use the library in anger.

Until last week, that is.

Doing so resulted in smoothing of the API and adding of some convenience features. It also bloated the code of the library from 35 LoC to 74 LoC (!)

The [code](https://gist.github.com/sustrik/305e9f6a768c582a0189bae5f5d327af) I have written generates some man pages and C header files.

Let me paste a snippet here so that you get a feeling how a real-world code written with tiles looks like:

    # SYNOPSIS section
    synopsis = t/'#include<@{fx["header"]}>'
    if fx["add_to_synopsis"]:
        synopsis |= t%'' | t/'@{fx["add_to_synopsis"]}'
    synopsis |= t%'' | t/'@{signature(fx)}'
    
    # DESCRIPTION section
    description = t/'@{fx["prologue"]}'
    if fx["protocol"]:
        description = t/'@{fx["protocol"]["info"]}' | t%'' | description
    if fx["experimental"] or (fx["protocol"] and fx["protocol"]["experimental"]):
        description = t/'**WARNING: This is experimental functionality and the API may change in the future.**' | t%'' | description
    if fx["has_iol"]:
        description |= t%'' | t/"""
            This function accepts a linked list of I/O buffers instead of a
            single buffer. Argument **first** points to the first item in the
            list, **last** points to the last buffer in the list. The list
            represents a single, fragmented message, not a list of multiple
            messages. Structure **iolist** has the following members:
    
            ```c
            void *iol_base;          /* Pointer to the buffer. */
            size_t iol_len;          /* Size of the buffer. */
            struct iolist *iol_next; /* Next buffer in the list. */
            int iol_rsvd;            /* Reserved. Must be set to zero. */
            ```
    
            When receiving, **iol_base** equal to NULL means that **iol_len**
            bytes should be skipped.
    
            The function returns **EINVAL** error in the case the list is
            malformed:
    
            * If **last->iol_next** is not **NULL**.
            * If **first** and **last** don't belong to the same list.
            * If there's a loop in the list.
            * If **iol_rsvd** of any item is non-zero.
    
            The list (but not the buffers themselves) can be temporarily
            modified while the function is in progress. However, once the
            function returns the list is guaranteed to be the same as before
            the call.
            """
    if fx["args"]:
        description |= t%'' | (t/'').vjoin([t/'**@{arg["name"]}**: @{arg["info"]}' for arg in fx["args"]])
    if fx["epilogue"]:
        description |= t%'' | t/'@{fx["epilogue"]}'
    if fx["protocol"] or fx["topic"] == "IP addresses":
        description |= t%'' | t/'This function is not available if libdill is compiled with **--disable-sockets** option.'
    if fx["protocol"] and fx["protocol"]["topic"] == "TLS protocol":
        description |= t%'' | t/'This function is not available if libdill is compiled without **--enable-tls** option.'
    
    # RETURN VALUE section
    if fx["result"]:
        if fx["result"]["success"] and fx["result"]["error"]:
            retval = t/"""
                In case of success the function returns @{fx["result"]["success"]}.
                'In case of error it returns @{fx["result"]["error"]} and sets **errno** to one of the values below.
                """
        if fx["result"]["info"]:
            retval = t/'@{fx["result"]["info"]}'
    else:
        retval = t/"None."
    
    # ERRORS section
    standard_errors = {
        "EBADF": "Invalid handle.",
        "EBUSY": "The handle is currently being used by a different coroutine.",
        "ETIMEDOUT": "Deadline was reached.",
        "ENOMEM": "Not enough memory.",
        "EMFILE": "The maximum number of file descriptors in the process are already open.",
        "ENFILE": "The maximum number of file descriptors in the system are already open.",
        "EINVAL": "Invalid argument.",
        "EMSGSIZE": "The data won't fit into the supplied buffer.",
        "ECONNRESET": "Broken connection.",
        "ECANCELED": "Current coroutine was canceled.",
        "ENOTSUP": "The handle does not support this operation.",
    }
    errs = {}
    for e in fx["errors"]:
        errs[e] = standard_errors[e]
    errs.update(fx["custom_errors"])
    errors = t/"None."
    if len(errs) > 0:
        errors = (t/'').vjoin([t/'* **@{e}**: @{desc}' for e, desc in sorted(errs.items())])
    if fx["add_to_errors"]:
        errors |= t%'' | t/'@{fx["add_to_errors"]}'
    
    # Generate the manpage.
    page = t/"""
             # NAME
    
             @{fx["name"]} - @{fx["info"]}
    
             # SYNOPSIS
    
             ```c
             @{synopsis}
             ```
    
             # DESCRIPTION
    
             @{description}
    
             # RETURN VALUE
    
             @{retval}
    
             # ERRORS
    
             @{errors}
             """
    
    # Add EXAMPLE section, if available.
    example = ""
    if fx["protocol"] and fx["protocol"]["example"]:
        example = t/'@{fx["protocol"]["example"]}'
    if fx["example"]:
        example = t/'@{fx["example"]}'
    if example:
        page |= t%'' | t/"""
            # EXAMPLE
    
            ```c
            @{example}
            ```
            """
    
    # SEE ALSO section.
    # It'll contain all funrction from the same topic plus the functions
    # added manually.
    sa = [f["name"] for f in topics[fx["topic"]] if f["name"] != fx["name"]]
    if fx["has_deadline"]:
        sa.append("now")
    if fx["allocates_handle"]:
        sa.append("hclose")
    if fx["protocol"] and fx["protocol"]["type"] == "bytestream":
        sa.append("brecv")
        sa.append("brecvl")
        sa.append("bsend")
        sa.append("bsendl")
    if fx["protocol"] and fx["protocol"]["type"] == "message":
        sa.append("mrecv")
        sa.append("mrecvl")
        sa.append("msend")
        sa.append("msendl")
    # Remove duplicates and list them in alphabetical order.
    sa = list(set(sa))
    sa.sort()
    #seealso = t/""
    #for f in sa:
    #    seealso += t/"**@{f}**(3) "
    seealso = (t%' ').join([t/'**@{f}**(3)' for f in sa])
    page |= t%'' | t/"""
        # SEE ALSO
    
        @{seealso}
        """
    
    with open(fx["name"] + ".md", 'w') as f:
        f.write(str(page))

Generally speaking, I am happy with the experiment.

I would like to highlight the following facts:

1\. There's no DSL in the code whatsoever. Not even a simple one.
2\. The source code is nicely indented.
3\. The generated code is nicely indented.
4\. There isn't a single escape sequence in the code.

On the other hand, there are some minor warts.

For example, when you want to join multiple strings in Python, you can do it this way:

    result = ",".join("circle", "square", "triangle")

When you want to join multiple tiles though you need an extra pair of parentheses:

    result = (t/",").join(t/"circle", t/"square", t/"triangle")

When you want to put one tile below another and separate them by a blank like you do it as follows:

    result = a | t%"" | b

The empty line literal (t%"") looks too much like a vim command.

However, both of these problems are artifacts of hacking the tile support on top of existing Python language rather than having the tile primitive type supported by the language itself. If there was native support for tiles, the code would look like this:

    result = t",".join(t"circle", t"square", t"triangle")
    
    result = a | w"" | b

**Feb 21st, 2019**
