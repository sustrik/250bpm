# A really hard problem



It's not that often that one encounters a really hard problem. Complex, yes, you deal with that daily. You have to integrate with different mutually imcompatible technologies, you keep bumping into edge cases and so on. But a problem that's hard in its essence, not very much so.

Hard problems are rare and precise. That's why I want to share the one I stumbled over recently. And, to warn you in advance, I have no freaking idea about the correct answer.

And here's the problem:

Have you ever had to make sense of an unfimiliar Java codebase? (If you have no Java experience, replace it with C++, or maybe with some other language, although Java fits the best.) You open some random file and look at the code. You see some abstract classes inheriting from interfaces and other abstract classes, some templates forwarding method calls to other templates and similar stuff. What you need is a line of code that actually does something, so that you can figure out what the program is supposed to do. However, finding such line is not an easy task. It looks like there's nothing but scaffolding everywhere.

Finally, you find a line of code that actually does something. However, it's alone in it's own function. There are other such lines in other mini-functions. And those functions are invoked via five layers of abstraction and it's not even clear how they fit together, whether one is invoked before another one or other way round. Or maybe they are independent and can easily run in parallel. You have no idea.

Anyway, you know what I am talking about.

Now, imagine that I am your grandmother and I ask you about your job. You show me some code, you show me a line that prints a message on a screen, another one that converts celsius to fahrenheit. And I (or your grandmother, really) ask: "What are all those other lines doing?"

And that's my hard question.

Just remember that I am your grandmother and you can't trick me by saying "it's abstraction" or something similarly vague. I don't know what abstraction is. I just want to know what are all those lines good for.

It's a week since I started to think about the problem and I still don't have a slightest clue. The only answer I was able to come with was an evolutionary one: The code that's good at reproducing reproduces. It doesn't have to be useful to be ubiquitous. But that's a defeatist answer. Surely there is at least some value for us programmers in those lines of code. But if so, what exactly is it?

**September 14th, 2015**