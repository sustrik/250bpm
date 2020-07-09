# Advanced metaprogramming in C



Metaprogramming in C is the art of creating new language constructs, typically using macros.

Great introduction to C metaprogramming by Simon Tatham can be found here:

[Metaprogramming custom control structures in C](http://www.chiark.greenend.org.uk/~sgtatham/mp/)

Recently, however, I've faced a problem that could not be solved by the means outlined in the article. I was implementing a control structure with variable number of clauses, similar to C's 'switch' statement. To be more concrete, I was trying to implement an equivalent of golang's 'select' statement in [libmill](http://libmill.org) project.

Here's how the statement looks like in golang:

    select {
    case channel1 <- 42:
        foo()
    case i := <- channel2:
        bar(i)
    }

The problem here is that the construct is stateful. It has to collect all the conditions first, then wait till one of them becomes true. At the first sight it looks like the syntax like this cannot be even implemented in C. One's natural instinct is to implement it in idiomatic C way by first creating an array of conditions, then doing the poll and finally executing particular piece of code based on the return value from the poll. Something like this:

    int i;
    struct select_condition conds[2];
    conds[0].channel = channel1;
    conds[0].operation = SELECT_OUT;
    conds[0].out_value = 42;
    conds[1].channel = channel2;
    conds[1].operation = SELECT_IN;
    conds[1].in_value = &i;
    switch(do_select(conds, 2)) {
    case 0:
        foo();
    case 1:
        bar(i);
    }

However, such syntax is ugly and verbose. You can tolarate it if you are a C programmer, but if you come from a different background you'll find it simply atrocious. Can we make it better in some way?

One obvious thougt would be to wrap the initialisation of the pollset into some handy macros:

    #define in(conds, index, chan, val)\
        conds[index].channel = chan;\
        conds[index].operation = SELECT_IN;\
        conds[index].in_value = &val;
    
    #define out(conds, index, chan, val)\
        conds[index].channel = chan;\
        conds[index].operation = SELECT_OUT;\
        conds[index].out_value = val;

The user's code would then look a bit simpler:

    int i;
    struct select_condition conds[2];
    out(conds, 0, channel1, 42);
    in(conds, 1, channel2, i);
    switch(do_select(conds, 2)) {
    case 0:
        foo();
    case 1:
        bar(i);
    }

So far, we've done nothing unexpected. But can we go further? Can we somehow not require the user to specify the size of the pollset in advance? It turns out that yes. It can be done using a technique that I am a proud inventor of: We can build a linked list on the stack!

EDIT: It have been pointed out that the linked-list-on-the-stack technique have already been around before this. That makes me a proud re-inventor! Yay!

    #define concat(x,y) x##y
    
    #define in(conds, chan, val)\
        struct select_condition concat(cond,__COUNTER__);
        concat(cond,__COUNTER__).channel = chan;\
        concat(cond,__COUNTER__).operation = SELECT_IN;\
        concat(cond,__COUNTER__).in_value = &val;\
        concat(cond,__COUNTER__).next = conds;\
        conds = &cond;
    
    #define out(conds, chan, val)\
        struct select_condition concat(cond,__COUNTER__);
        concat(cond,__COUNTER__).channel = chan;\
        concat(cond,__COUNTER__).operation = SELECT_OUT;\
        concat(cond,__COUNTER__).out_value = val;\
        concat(cond,__COUNTER__).next = conds;\
        conds = &cond;

And here's the user's code. Note that do\_select() is now getting a linked list as an argument instead of an array. Also note that the linked list doesn't have to be deallocated because it lives on the stack and will be freed automatically at the end of the function:

    int i;
    struct select_condition *conds = NULL;
    out(conds, channel1, 42);
    in(conds, channel2, i);
    switch(do_select(conds)) {
    case 0:
        foo();
    case 1:
        bar(i);
    }

At this point we would like to rearrage the code in such a way the actions — foo() and bar() — are collocated with the conditions that trigger them rather then having all the conditions listed first, followed by all the actions.

Once again, this looks like it may not be possible. Macros are strictly local. They cannot move pieces of code up or down the source file.

But that kind of obstacle cannot stop a dedicated C hacker! If we can't move the code, let's do it in a dynamic fashion. We'll introduce a loop with two iterations. First iteration will build the linked list, second one will execute the action:

    int i;
    int result = -1;
    struct select_condition *conds = NULL;
    while(1) {
    
        if(result == - 1) {
            out(conds, channel1, 42);
        }
        if(result == 0) {
            foo();
            break;
        }
    
        if(result == - 1) {
            in(conds, channel2, i);
        }
        if(result == 1) {
            bar(i);
            break;
        }
    
        result = do_select(conds);
    }

Nice, except that it doesn't work.

The problem is that in() and out() macros declare a local variable (select\_condition) which gets out of scope when the surrounding if block finishes. Which means that the value can be overwritten at any time. What we need is to get rid of those if blocks. And, yes, we are going to use gotos to accomplish that. Oh boy, this is going to get ugly! But keep calm and follow me!

    int i;
    int result = -1;
    struct select_condition *conds = NULL;
    while(1) {
    
        if(result != -1)
            goto label0;
        out(conds, channel1, 42);
        label0:
        if(result == 0) {
            foo();
            break;
        }
    
        if(result != -1)
            goto label1;
        in(conds, channel2, i);
        label1:
        if(result == 1) {
            bar(i);
            break;
        }
    
        result = do_select(conds);
    }

Now let's stuff more code into in and out macros to make the user's code simple:

    #define select \
        int result = -1;\
        struct select_condition *conds = NULL;\
        while(1)
    
    #define in(chan, val) in_((chan), (val), __COUNTER__)
    #define in_(chan, val, idx)\
        if(result != -1)\
            goto concat(label, idx);\
        struct select_condition concat(cond, idx) =\
            {chan, SELECT_IN, &val, 0, conds};\
        conds = &cond;\
        concat(label, idx);\
        if(result == idx)
    
    #define out(chan, val) out_((chan), (val), __COUNTER__)
    #define out_(chan, val, idx)\
        if(result != -1)\
            goto concat(label, idx);\
        struct select_condition concat(cond, idx) =\
            {chan, SELECT_OUT, NULL, val, conds};\
        conds = &cond;
        concat(label, idx);\
        if(result == idx)
    
    #define end \
        result = do_select(conds);

Note that we had to split the macros into two so that we can reuse the same value of \_\_COUNTER\_\_ in multiple places.

And here is how the user code looks like:

    int i;
    select {
        out(channel1, 42) {
            foo();
            break;
        }
        in(channel2, i) {
            bar(i);
            break;
        }
        end
    }

There's some more polishing to do. We can get rid of the break statements by hiding them in the following macro. We can declare 'i' varaible in directly in the out() macro. We should put the whole statement into a code block so that variables like 'conds' don't pollute the surrounding namespace.

These final touches are left as an exercise for the reader. (If out of your wits, you can check real-world implementation of the construct [here](https://github.com/sustrik/libmill/blob/41504d5b7816e4fd152b11d07309c5e9ccfdfb3d/libmill.h#L175).)

Have fun and happy Swiss National Day everyone!

**August 1st, 2015**