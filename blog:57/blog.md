# Document intent not algorithm: A use case



It's often said that when writing comments you should document intent rather than algorithm.

However, I think lot of programmers haven't really grasped the maxim. Therefore, I was trying to come up with a minimal use case, an example that would illustrate, in very simple and easy to remember way, why that is the case.

Imagine you are debugging an application written by someone else. You have little understanding of how it works, what are the data structures or algorithms and so on.

When you look at the block of code that is the likely culprit, there are two lines like this:

    /* Increment orderid. */
    orderid++;

Ok, so some kind of order ID is being incremented here. Everything works as expected, right?

Well, imagine that the code was written in a slightly different way:

    /* Get next order ID. */
    orderid++;

Aha. That makes it more interesting. Is the next order ID the one with ID+1? Maybe the orders are ordered in decreasing sequence and the code should have been:

    /* Get next order ID. */
    orderid--;

You investigate some more and yes, it turns out that while the order IDs are increasing there may be holes in the sequence because of cancelled orders.

And here's the fix:

    /* Get next order ID. */
    while(1) {
        orderid++;
        if(is_valid_order(orderid))
            break;
    }

The example above was deliberately trivial. It may seem at first glance that the different between "increment" and "get next" is insignificant. However, once the code grows sufficiently complex, such clarity in expressing the intent can make a world of difference.

**August 3rd, 2015**