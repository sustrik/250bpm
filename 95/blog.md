# Linguistics and Programming Languages



NOTE: This is an article I've published more that a decade ago. From my today's point of view it may be a bit naive but it still makes a valid and interesting proposal. Sadly though, nobody have taken the challenge in the meantime. Can it be a time to do so now? I am republishing it here as is, with no modifications whatsover.

It is quite common to use computers to analyse natural languages. Although we are not yet able to accomplish the task plausibly, the problem is being solved with the hope that one day we will be able to communicate with computers in natural language.

Other way round, programmers have to speak 'computerish'. We are able to 'speak' C, Pascal, SQL or even machine code. We learn a computer language using the same faculties as learn our own human language, in intuitive manner, without a profound understanding of what is going on in out brain.

It looks like both approaches have the same goal: to allow people and computers to communicate freely. However, both are quite extreme. Former approach wants to teach computers to speak English, not taking into account that computers are not humans and therefore cannot speak English, or at least cannot speak proper, complex, human English, full of subtleties and ambiguities. Latter approach wants humans to speak completely computerish (at least when talking about machine code - other programming languages are bit more human-friendly) and fails to recognise that humans are not computers and often have problems dealing with things that look really simple from the computer's point of view.

It is clear that the solution will lie somewhere in-between these extremes. We will not speak to computers using hexadecimal machine code, nor will computers answer in Shakespearean English. The compromise will be natural-language-like enough for people to use it freely without need to spend big amounts of time just to figure out how the code should look like and in the same time exact enough for computers to parse it unambiguously in reasonable time.

The goal of this article is not to make a proposal of this kind of language. If it exists at all, it will be created through long process of evolution, the same way as natural languages evolved. It is not in single person's capacities to design it, nor will it be a single unique language. However, we may look at computer languages as well as on natural languages, compare them and try to figure out what are the differences, why they are there and what kind of problems they are pointing to.

We may do that just by looking at problems we have in computer language design and asking: "How is the problem solved in natural language? Does it give any hint on how to solve it in computer language?" Although this approach alone would give us big amount of interesting results, the problem with it is that there is a lot of problems in computer languages that we are not even aware of, that we don't think about, that we consider to be something unavoidable in its nature.

So we may follow the opposite way. Looking at natural language we may ask: "What is this construction used for? Do we have a need to express something similar in computer language? How do we express it then? Is computer language construct easy to write and understand or is it just an annoyance, when compared to corresponding one in the natural language? If so, is it possible to introduce the natural language construct into programming language?"

In this article I will use mixed approach. It will be just a simple show-and-tell. I will take a simple programming construction, analyse it from linguistic point of view and try to suggest possible improvements. I will call this hypothetical 'improved' C language 'C-ish' to emphasise its tie to natural languages.

Although a more comprehensive study would be able to contain more information and cover the area in a more precise way, I believe that giving very straightforward examples like the ones below without loads of theory is essential for computer scientists without linguistic background to get a grip of the subject. So here we go:

C-ish
-----

Identifying semantic and syntactic roles in a method call 'Semantic role' of a phrase in a sentence means its relationship to the overall meaning of the sentence. For example, a phrase may be an 'action', i.e. what is going on in sentence. Or it may be an 'agent', the performer of the action. In following example 'peter' is an agent while 'walks' is an action.

    English: Peter walks.

Each phrase has also its syntactic role. In aforementioned case, 'peter' is a subject and 'walks' is a predicate. However, it is necessary to keep in mind that there is no one-to-one correspondence between semantic and syntactic roles.

There are some intuitively felt common roles in natural language sentence and in method call statement in a programming language. First of all it is the concept of 'action'. In natural languages this role is performed by a verb (a predicate). In programming languages, same role is taken care of by method name.

    English: Peter walks.
    C:         walk (peter);

In English version of the sentence 'Peter' plays the role of 'actor' (called 'subject' in linguistic terminology). As for C 'peter' has no special role. It is just one of the arguments of the function 'walk'. However, when the example is rewritten into C++, we will see that there is a special syntactic construction to mark the subject. In fact, one of the biggest differences between object-oriented and non-object-oriented programming is the possibility to identify the actor of an action using purely syntactic means.

    C++:     peter.walk ();

As for syntactic roles, there is no more of them in programming languages. In natural languages on the other hand we can find quite a lot of them. Now the question is: Are there more semantic roles (apart of 'action' and 'actor') in programming languages that would profit from being formalised via explicit syntactic constructions? I would say there are. Say an 'index'. Argument of this type appears in quite a lot functions.

    C++:     container.insert (position, value);

If there was a special syntactic role for 'index' in programming languages, the call may look like this:

    C-ish:   container.insert [position] (value);

Compare it with equivalent construction in English. Preposition 'in' plays the same role as '\[\]' - namely identifying the place where the action takes place.

    English: Peter walks in the park.

We can identify arbitrary number of semantic roles this way. (Few examples: destination, source, range-beginning, range-end, etc.) However, we should keep in mind that not all the semantic roles, even in natural languages, have their syntactic counterparts. Sometimes several semantic roles are expressed using same syntactic role, depending on context to resolve the ambiguity, sometimes descriptive phrases are used to express certain semantic role. Number of syntactic roles should be kept low not to overcomplicate the grammar of the language.

Now let's have a look at syntactic roles in natural languages. Apart of subject and predicate (which are already present in object-oriented languages, as we have seen) there is one special role present in all of them, one playing the key role (together with subject and predicate) in the grammar. It is the role called 'object', i.e. the entity the action is performed on.

    English: Peter hits David.
             Peter picks a key.

Most of the functions encountered in programming languages do have a clear object:

    C++:     my_file.open ("log.txt", ios_base::openmode::in);

(What is the action 'open' performed on? It is performed on the 'log.txt' file. It follows that it is the object of the statement.)

At this point I will abandon the subject of the syntactic roles. However, in what follows I will need to use 'object' role, so let's devise following construction to formalise it. I chose a colon sign for this as it resembles dot sign used for separating subject and predicate. This way, standard subject-verb-object statement can be written as follows:

    C-ish:   peter.hit:david;

Conjunction
-----------

In natural languages, phrases of same kind can be grouped using conjunctions.

    English: Peter and Jack hit David.
             Peter hits and injures David.
             Peter hits David and Jack.

There is no equivalent of this in programming languages, however, every programmer, in case he have learned to program by himself, had probably attempted to use naturally looking but disallowed conjunction at some point:

    C:       *if (a > 0 && < 10) ...

(Note: In linguistics, asterisk in front of a phrase is used to mark the phrase as ungrammatical.)

The line cannot be compiled, of course.

Looking into the manual, or maybe just experimenting with the statement, he found out that the construct should look like this:

    C:       if (a > 0 && a < 10) ...

He corrected the line without giving it much thought and forgot about the problem completely.

If asked about the former construct in the time, when he grew more experienced, he would probably say that the construction is not allowed because it is kind of vague and ambiguous, but, if needed, it can be built into compiler without any problems as it is only 'syntactic sugar', something that makes programmer's life easier, but has no special meaning by itself.

However, if he is asked to implement this feature, he would run into really serious problems.

We would expect following three statements to be semantically equivalent:

    C-ish: if (a < b & a < c) ...
           if (a < b & < c) ...
           if (a < b & c) ...

But what should the compiler do to interpret such expressions? Have a look at conjuncted clauses. How would we interpret them in terms of programming language? First conjuncted clause has clear semantics, but what about the second and the third one? What is conjuncted subexpression '< b' supposed to mean? Is it a function that compares its argument to b? And what about 'b & c'? Is it a way to construct a set? If so, operator '<' would have different semantics in each of the examples. In first one it is a standard comparison between two numbers. In second one it is a way to create an unary function. In third one it is a comparison between a number and a set of numbers. Same applies to '&'. In the first case it is a standard logical AND. In second one it is a way to combine two unary functions. In third one it creates a set of numbers.

All these subtleties seem to be too complex to express so simple a concept as joining two parts of an expression by 'and'. Are we following a wrong way? Thinking in terms of orthodox compiler design yields no sensible answer.

So let's have a look at the problem from different point of view. But first, let's make an equivalent example with explicit function calls (bear in mind that '<' is only a shortcut for function 'operator <'):

    C-ish: list & another_list . insert : x ;
           list . erase & insert : x ;
           list . insert : x & y ;

Same parsing problem as we described persists in this example. What we should focus on, is the fact that natural language cannot be described solely by means of context-free grammar. In fact, context-free grammar plus set of transformation rules (non-context-free) is used to perform the task. Once we got rid of context-freeness constraint, the problem begins to give sense. (Note: 'Non-context-free' sounds scary. It gives an idea of greater complexity of parsing that we can afford. However, there is a lot of simple transformations that can be parsed quickly even though they are inherently non-context-free.)

First of all let's think of '.' as a prefix identifying that the subsequent identifier is the predicate. Same for ':'. This prefix identifies the following identifier as the object. Identifiers without a prefix (Φ-prefix) are to be considered subjects.

Next, '&' would mean that the role of subsequent identifier is the same as that of the preceding one in conjunction.

Using this transformation we would get following sequences (we are using minus sign to join prefix with the identifier it applies to):

    C-ish: Φ-list Φ-another_list .-insert :-x ;
           Φ-list .-erase .-insert :-x ;
           Φ-list .-insert :-x :-y ;

Now we will interpret sequences like these as standing for all possible combinations of their subjects, predicates and objects. So for example having a statement with two subjects, three predicates and four objects, it would be expanded into 2 x 3 x 4 = 24 separate statements, each having single subject, predicate and object.

    C-ish: Φ-list .-insert :-x ;
           Φ-another_list .-insert :-x ;v
           Φ-list .-erase :-x ;
           Φ-list .-insert :-x ;
    
           Φ-list .-insert :-x ;
           Φ-list .-insert :-y ;

In plain C-ish (without the prefixes attached to their identifiers) it would look like this:

    C-ish: list . insert : x ;
           another_list . insert : x ;
    
           list . erase : x ;
           list . insert : x ;
    
           list . insert : x ;
           list . insert : y ;

And that is exactly what was meant by original example, this time without the use of conjunctions.

The problem is more complicated, of course. The simplistic algorithm used above certainly does not match the way how conjunctions are parsed in natural languages. We should, for example, be able to conjunct whole predicate-object pairs (i.e. 'verbal phrases' as they are known in linguistics) apart of simple predicate conjunction.

In fact, this predicate-only conjunction we see in the C-ish example is considered to be an advanced feature of language (called 'right node raising') when compared to standard verbal phrase conjunction, that there is no support for in the example. However, problems like this one are out of scope of this article.

More transformations: Passivisation
-----------------------------------

Adding conjunctions to standard programming language looks trivial but once it is introduced, other natural language concepts that seem to have no counterpart in programming languages begin to give sense. For all, take an example of passivisation. In natural language you can rephrase the sentence using passive voice:

    English: I took it.
             It was taken by me.

There is really nothing similar in programming languages, but once you start to use the conjunction construct I just introduced, you will encounter following problem. When you want to get string s to uppercase and append it by string t, you can do it in following way:

    C-ish:   s . upper & append : t ;

However, when you want to get s to uppercase and append it to t, you will have to split the action into two statements:

    C-ish: s . upper ;
           t . append : s ;

Now let's suppose there exists a passivisation operator '@' that modifies function in the way that it will exchange syntactic positions of subject and object. This way following statements will be equivalent.

    C-ish:   t . append : s ;
             s . @ append : t ;

Having this kind of construction allows expressing the upper/append example in a single statement.

    C-ish:   s . upper & @ append : t ;

This example demonstrates how constructs of natural language may be introduced into programming language. However, it is also an example of risks to be faced by doing so.

Although passivisation in this form looks very simple and elegant, it does not occur in any natural language I am aware of. Normally, object is turned to subject; however, subject is not turned to direct object. It is instead promoted to some other syntactic role:

    English  *It was taken me.
             It was taken by me.

In English preposition 'by' is used to identify the actor. In most Slavic languages special case (instrumental) is used for the same purpose. In some other languages, like modern Arabic, idiomatic expression is used instead ('min qiblii' = 'from my side').

This fact may mean that elegant swap-the-roles passivisation construction as I have introduced it, may be felt as unnatural and hard-to-understand by programmers.

However, it may be even worse than that. Looking at the natural languages it may be seen that although passive with actor specified exists, it tends not to be used commonly and is often viewed as purely literary construct. Most occurrences of passive in common language are used to express that actor is either unknown or irrelevant, or, in syntactic terms, to turn transitive verb into intransitive one.

    English: It was broken.

The point here is to understand that unreasonable introduction of natural-language traits into programming languages may bring not only benefits, but problems as well.

Conclusion
----------

As we have seen, applying analogy with natural languages to programming languages may yield quite interesting results. I have deliberately restricted myself to syntax, as this is the only field of linguistics that is felt to be integral part of computer science. However there are still other fields that can give equally interesting results. Semantics, morphology or lexicology, for example.

Here are some more problems of interest:

*   How does natural language avoid infix recursion (for example subordinate sentences in the middle of main sentences)?
*   Is it possible to use this mechanism in programming languages to avoid unreadable clusters of nested function calls, nested loops etc.?
*   How does natural language distinguish between known and newly introduced entities?
*   How does programming language accomplish the same task?
*   Is there a correspondence between indefinite/definite article and variable declaration/reference?
*   How can natural language do without local variables, i.e. creating an individual name for every single thing we are speaking about?
*   If the definite article and pronouns is the answer, is it possible to get rid of local variables in programming language as well?
*   How can we deal with the problem of naming sets of closely related entities without resorting to names as 'entity', 'entity2', 'entityEx', '\_entity' etc.?
*   There are languages that are able to generate hundreds of regular forms with clear semantics from a single stem. Are we able to do the same in programming languages?
*   What is agglutination and are we using it without knowing it in formalisms like Hungarian notation?
*   Is there a lexis of programming languages?
*   Does STL documentation correspond to a dictionary of natural language?

Many of these questions are still to be explored. On the way we may obtain completely different view of what a programming language might be and how they could be analysed and improved.