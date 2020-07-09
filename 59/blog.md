# OO languages spend most effort addressing a minority use case



Programming language design must take many aspects into consideration. Fitting it's target domain, performance, style and so on.

One aspect I am personally most interested in is expressivity. Specifically: If I take a diagram from my sketchbook, is there a way to express it in the language? If I draw two boxes connected by an arrow, is there any way to capture the relationship in the language itself or do I have to resort to comments?

For example, SQL is good at expressing cardinality: For one element of this type there can be N elements of that type. Object oriented languages, on the other hand, nicely cover the "is-a" relationship: Dog is an animal. class Dog extends Animal.

Yesterday I went through my old sketchbooks and realised an interested thing: Only a little minority of diagrams (roughly 5%) were drawn to express "is-a" relationship. I am not a taxonomist, after all.

The majority of diagrams expressed communication flows, things like: "Component A speaks to component B, but not to component C."

Of course, this may be the case just for me. Perhaps majority of programmers fill their scratchbooks with class hierarchies. I doubt it, but if I am wrong, I would love to hear about it.

So, if what I said applies to most programmers, then the following is true:

**Object oriented languages spend most effort addressing a minority use case.**

The use case is cherished and compilers are made to discover any problems with it in compile time and produce nice error messages. At the same time other use cases are ignored, programmers have to ensure their consistency manually, by runtime checks or, even worse, by putting the constaints into comments or design documents. OO folks are wasting their time discussing minutiae of their little peculiar use case, such as, say, single vs. multiple inheritance, while at the same time nobody is paying attention to what is needed in majority of cases.

I've already written about why I switched from C++ to C ([here](http://250bpm.com/blog:4) and [here](http://250bpm.com/blog:8)) but the most fundamental reason it all boils down to is: If a complex language doesn't allow me to express 95% of what I would like to I can very well use a simpler language and save myself the headache.

Now, how are we going it fix that? And does anybody even care?

* * *

On a tangential: Have you noticed that natural languages have very little resemblance to [John Wilkins' analytical language](https://en.wikipedia.org/wiki/An_Essay_towards_a_Real_Character_and_a_Philosophical_Language)? Once again, taxonomy is one of least concerns of a user of a natural language. The fact that marmot is a rodent is simply not that interesting. You want to say what happened, express your intentions, give orders, ask questions. You want to go on with your life.

Another tangential: Despite all the misguided focus on taxonomy there's one awesome thing that OO languages have introduced: Singling out one of the function's parameters (this, self) and putting them to a syntactically special position:

    arg1.function(arg2, arg3, arg4);

I've written about it [here](http://www.ppig.org/news/2006-06-01/linguistics-and-programming-languages). Bear in mind that it's an article from 2006 and talks about reserach done mostly in late 1990's. I have to write something more up-to-date: If nothing else, I should mention Go's approach to the problem.

**Martin Sústrik, August 15th, 2015**