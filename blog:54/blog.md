# The Second Use Case for Literate Programming



Everyone have heard that Donald Knuth have invented something called "literate programming". Everybody thinks that it's something like commenting your code very heavily, but maybe not — maybe it's different in some way. [Wikipedia](https://en.wikipedia.org/wiki/Literate_programming) isn't of much help. Nobody is quite sure.

To understand what's going on, you have to remember what Mr. Knuth does for living: He's an academic. He writes papers and textbooks.

And how does a paper about computer science look like? It's nicely formated text, with chapters and figures and equations and snippets of code.

One writes such papers in TeX.

But there's a problem: How would you know that the program you are presenting would actually compile and run? It's a paper after all, you can't just take it and compile it.

Enter literate programming.

You write the document in a language that makes it easy to extract the snippets of code from the paper and reassemble them to form a full-blown program.

That's why there are two seemingly unrelated aspects of literate programming. First, there's a way to distinguish the document (TeX source) and the code (C, for example). Second, there's a simple template language to specify how do the individual snippets of code fit together.

Easy. Almost trivial. And yet unexpected and beautiful in its own way.

And it's also obvious why the literate programming haven't got much traction: Only minority of programmers works on complex algorithms and publishes papers and textbooks about them. Most programmers write CRUD applications. Or whatever is the latest and shiniest counterpart of CRUD nowadays. When writing CRUD, there's no need for extensive explanation of what the code does. It does CRUD. As simple as that.

Actually, there's an influential train of thought among programmers which argues that extensive documentation in the code is necessarily going to bitrot and turn into a maintainability problem. Programmers with such disposition try to keep the comments in code at minimal level and focus on writing self-documenting code (using descriptive variable names and such).

In any case, I've recently realised that there's a different niche outside of academia where literate programming would make sense.

It's the niche of complex processes which are not very exact or well understood, processes which change often but are executed rarely.

Consider, for example, a program that does yearly report for a big IT department.

IT changes a lot. The program is run on Jan 1st and after a year, when it is supposed to be run again, it no longer works. All the systems it interfaced with have changed. The API is different and the program doesn't even compile. It references database tables that were either heavily refactored or don't even exist anymore. The tools it used to perform its task no longer work. Licenses may have expired or the vendor have simply stopped supporting them. And so on.

In short, it can be said that the program is functional only once a year, on January 1st. The rest of the year it is broken.

Or you can put it in a different way: You can say that program execution and debugging blend to such extent that it's hard to tell the difference between the two.

How would you go about writing such a program?

Writing neat and perfectly polished code doesn't make sense. The program will bitrot almost immediately after it is exectuted anyway. What makes sense though, is documententing the **intent** of the code in a great detail. The programmer tasked with running the program next year will not make much sense of the broken code. References to APIs and tables that don't exist anymore will confuse him more than help him. However, he will greatly benefit from the lengthy description of what the code is **intended** to do.

That's why literate programming may help in this case.

However, I don't believe that tools Mr. Knuth and his associates have written would be of much help here. The use case is sufficiently different that, although it still can be recognised as literate programming, it needs either extended or completely different tools. I can't imagine engineer documenting the yearly balance program in TeX. Markdown seems to be a much more realistic option. Also, tying the tool to a single programming language probably won't work. Complex processes in most cases need to use a large number of disparate technologies and even pass the execution to the human being at times (e.g. "press the power button") and we have to account for that.

I am still thinking about how to solve this problem. It's extremely interesting because it requires redefining the very interface between the machine and the programmer. Instead of programmer writing the program and machine executing it afterwards we now have them participating on a single continuous process, programmer providing his ability to deal with the unexpected, machine supplying the raw computational power. Such systems are not unheard of (Prolog, anyone?) but they've rarely went beyond being an academic exercise. And maybe it's time to change that.

**July 20th, 2015**