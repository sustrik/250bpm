# Why should I have written ZeroMQ in C, not C++ (part I)



Just to be clear from the very beginning: This is not going to be a Torvalds-ish rant against C++ from the point of view of die-hard C programmer.

I've been using C++ whole my professional career and it's still my language of choice when doing most projects.

Naturally, when I started ZeroMQ project back in 2007, I've opted for C++. The main reasons were:

1.  Library of data structures and algorithms (STL) is part of the language. With C I would have to either depend on a 3rd party library or had to write basic algorithms of my own in 1970's manner.
2.  C++ enforces some basic consistency in the coding style. For example, having the implicit 'this' parameter doesn't allow to pass pointer to the object being worked on using several disparate mechanisms as it often happens to be the case with C projects. Same applies to explicit marking of member variables as private and many other features of the language.
3.  This point is actually a subset of the previous one, but it's worth of explicit mention: Implementing virtual functions in C is pretty complex and tends to be slightly different for each class which makes understanding and managing the code a pain.
4.  And finally: Everybody loves destructors being invoked automatically at the end of the block.

Now, almost 5 years later, I would like to publicly admit that using C++ was a poor choice and explain why I believe it is so.

First, it's important to take into account that ZeroMQ was intended to be a piece of infrastructure with continuous uptime. It should never fail and never exhibit undefined behaviour. Thus, the error handling was of utmost importance. It had to be very explicit and unforgiving.

C++ exceptions just didn't fill the bill. They are great for guaranteeing that program doesn't fail — just wrap the main function in try/catch block and you can handle all the errors in a single place.

However, what's great for avoiding straightforward failures becomes a nightmare when your goal is to guarantee that no undefined behaviour happens. The decoupling between raising of the exception and handling it, that makes avoiding failures so easy in C++, makes it virtually impossible to guarantee that the program never runs info undefined behaviour.

With C, the raising of the error and handling it are tightly couped and reside at the same place in the source code. This makes it easy to understand what happens if error happens:

    int rc = fx ();
    if (rc != 0)
        handle_error ();

With C++ you just throw the error. What happens then is not at all obvious:

    int rc = fx ();
    if (rc != 0)
        throw std::exception ();

The problem with that is that you have no idea of who and where is going to handle the exception. As long as the handling code is in the same function the error handling often remains more of less sane although not very readable:

    try {
        ...
        int rc = fx ();
        if (rc != 0)
            throw std::exception ("Error!");
        ...
    catch (std::exception &e) {
        handle_exception ();
    }

However, consider what happens when there are two different errors thrown in the same function:

    class exception1 {};
    class exception2 {};
    
    try {
        ...
        if (condition1)
            throw my_exception1 ();
        ...
        if (condition2)
            throw my_exception2 ();
        ...
    }
    catch (my_exception1 &e) {
        handle_exception1 ();
    }
    catch (my_exception2 &e) {
        handle_exception2 ();
    }

Compare that to its C equivalent:

    ...
    if (condition1)
       handle_exception1 ();
    ...
    if (condition2)
       handle_exception2 ();
    ...

It's far more readable and — as a bonus — compiler is likely to produce more efficient code.

However, it doesn't end there. Consider the case when the exception is not handled in the function that raises it. In such case the handling of the error can happen anywhere, depending on where the function is called from.

While the possibility to handle the exceptions differently in different contexts may seem appealing at the first sight, it quickly turns into a nightmare.

As you fix individual bugs you'll find out that you are replicating almost the same error handling code in many places. Adding a new function call to the code introduces that possibility that different types of exceptions will bubble up to the calling function where there are not yet properly handled. Which means new bugs.

If you don't give up on the "no undefined behaviour" principle, you'll have to introduce new exception types all the time to distinguish between different failure modes. However, adding a new exception type means that it can bubble up to different places. Pieces of code have to be added to all those places, otherwise you end up with undefined behaviour.

At this point you may be screaming: That's what exception specifications are for!

Well, the problem is that exception specifications are just a tool to handle the problem of exponential growth of the exception handling code in a more systematic manner, but it doesn't solve the problem itself. It can even be said it makes it worse as now you have to write code for the new exception types, new exception handling code \*and\* new exception specifications.

Taking the problems described above into account I've decided to use C++ minus exceptions. That's exactly how ZeroMQ and Crossroads I/O looks like today.

Unfortunately, the problems don't end up here…

Consider what happens when initialisation of an object can fail. Constructors have no return values, so failure can be reported only by throwing an exception. However, I've decided not to use exceptions. So we have to go for something like this:

    class foo
    {
    public:
        foo ();
        int init ();
        ...
    };

When you create an instance of the class, constructor is called (which cannot fail) and then you explicitly call init function (which can fail).

This is more complex that what you would do with C:

    struct foo
    {
        ...
    };
    
    int foo_init (struct foo *self);

However, the really bad thing about the C++ version of the code is what happens when developers put some actual code into the constructor instead of systematically keeping the constructors empty.

If that's the case a special new object state comes into being. It's the 'semi-initialised' state when object has been constructed but init function haven't been called yet. The object (and specifically the destructor) should be modified in such a way as to decently handle the new state. Which in the end means adding new condition to every method.

Now you say: But that's just a consequence of your artificial restriction of not using exceptions! If exception is thrown in a constructor, C++ runtime cleans the object as appropriate and there is no 'semi-initalised' state whatsoever!

Fair enough. However, it's beside the point. If you start using exceptions you have to handle all the exception-related complexity as described in the beginning. And that is not a reasonable option for an infrastructure component with the need to be very robust in the face of failures.

Moreover, even if initialisation wasn't a problem, termination definitely is. You can't really throw exceptions in the destructor. Not because of some self-imposed artificial restrictions but because if the destructor is invoked in the process or unwinding the stack and it happens to throw an exception, it crashes the entire process.

Thus, if termination can fail, you need two separate functions to handle it:

    class foo
    {
    public:
        ...
        int term ();
        ~foo ();
    };

Now we are back to the problem we've had with the initialisation: There's a new 'semi-terminated' state that we have to handle somehow, add new conditions to individual member functions etc.

    class foo
    {
    public:
        foo () : state (semi_initialised)
        {
             ...
        }
    
        int init ()
        {
            if (state != semi_initialised)
                handle_state_error ();
            ...
            state = intitialised;
        }
    
        int term ()
        {
             if (state != initialised)
                 handle_state_error ();
             ...
             state = semi_terminated;
        }
    
        ~foo ()
        {
             if (state != semi_terminated)
                 handle_state_error ();
             ...
        }
    
        int bar ()
        {
             if (state != initialised)
                 handle_state_error ();
             ...
        }
    };

Compare the above to the C implementation. There are only two states. Not initialised object/memory where all the bets are off and the structure can contain random data. And there is initialised state, where the object is fully functional. Thus, there's no need to incorporate a state machine into the object:

    struct foo
    {
        ...
    };
    
    int foo_init ()
    {
        ...
    }
    
    int foo_term ()
    {
        ...
    }
    
    int foo_bar ()
    {
        ...
    }

Now consider what happens when you add inheritance to the mix. C++ allows to initialise base classes as a part of derived class' constructor. Throwing an exception will destruct the parts of the object that were already successfully initialised:

    class foo : public bar
    {
    public:
        foo () : bar () {}
        ...
    };

However, once you introduce separate init functions, the number of states starts to grow. In addition to uninitialised, semi-initialised, initialised and semi-terminated states you encounter combinations of the states. As an example you can imagine a fully initialised base class with semi-initialised derived class.

With objects like these it's almost impossible to guarantee predictable behaviour. There's a lot of different combinations of semi-initialised and semi-terminated parts of the object and given that failures that cause them are often very rare the most of the related code probably goes into the production untested.

To summarise the above, I believe that requirement for fully-defined behaviour breaks the object-oriented programming model. The reasoning is not specific to C++. It applies to any object-oriented language with constructors and destructors.

Consequently is seems that object-oriented languages are better suited for the environments where the need for rapid development beats the requirement for no undefined behaviour.

There's no silver bullet here. The systems programming will have to live on with C.

By the way, I've started experimenting with translating ZeroMQ into C lately. The code looks great!

EDIT: The endeavour evolved into a new project called _nanomsg_ in the meantime. Check it [here](http://nanomsg.org).

Read [part II of the article](/blog:8).

**Martin Sústrik, May 10th, 2012**