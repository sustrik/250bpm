# Reputation Engineering, part III



In [the previous post](http://250bpm.com/blog:94) I have argued that reputation engineering can be done in any system with tokens that allow for accumulation of reputation. The example given were Twitter accounts that can be used for accumulating followers. In this post I want to dig deeper into the nature of reputation and reputation tokens.

Let me start with the trademark law. There are several advantages to using it as an example: It was created specifically to deal with reputation. It's been around for a long time which, one would hope, made it reflect actual needs and concerns in the area. Furthermore, being a law, it's highly formalized. And finally, it's not necessarily tied to computers or online economy which is helpful for getting a bigger picture.

When you come from an area such as programming, or really from any area of today's highly economy-centric society, you have a vague idea of trademarks being like Internet domain names. You buy a name and it's yours. It's your property and if anyone tries to use it you'll sue the pants off them.

Then it comes as surprise that trademark law is not at all like that.

First of all, you don't buy a trademark. Trademark is rather created as a by-product of using a name. You establish a company called "FooBar Engineering". You start offering services. Maybe you do a little advertising. People start to recognize the brand. And voilà, you own a legally recognized trademark. No explicit action on your part is needed.

Similarly, if you stop using the name, your claim to the name gradually dissipates. If you tried to enforce a trademark that you haven't used for decades, you would be laughed out of the court.

There is also the concept of "trademark goodwill" which loosely translates to "reputation". Interestingly, trademark goodwill tends to be explained in economic terms: It is the part of the value of the business that is gained through owning the trademark. In other words, it is the difference of prices if you sold the company with and without the trademark, respectively.

Another common misconception about trademarks is that the names are, similarly to Internet domain names, global.

In reality, the scope of trademark is limited to the area of one's activity. To give an often used example, Apple, the grocery store doesn't infringe on the trademark of Apple, the consumer electronics manufacturer. One can also imagine spatial limits, although, to my knowledge, these are not codified in law: Apple grocery in Great Sampford, UK doesn't infringe on the trademark of Apple grocery in Falmouth, Jamaica.

That's a rough summary, but of course, law is never simple and you should look at the real thing rather than relying on my idealized model. That being said, what can we make of all that?

First of all, reputation tokens, such as trademarks, are not scarce. All you need to do to own one is to start using it. If you want to own thousand trademarks you just go for it. It won't cost you a single cent.

In fact, if you wanted to devise a theory of reputation the most elegant option would be to claim that creation of a reputation token is a private act, done by a single person with no interaction with the outside world, similar to, say, creation of a keypair in cryptography.

The token can then be used as a vessel to store reputation.

The reputation itself is scarce — as witnessed by "trademark goodwill" being expressed in monetary terms.

It's pretty obvious that goodwill is actually the reputation associated with the trademark stored in brains of people all around the world. Just imagine what Coca-Cola would be if it lost it's trademark goodwill: Just another soda-producing company. In this case the goodwill, the fact that everyone knows and prefers Coca-Cola to any similar beverages, may be the biggest part of the value of the company.

But not so fast! The fact that your company comes first in Google search results for your area of business is a big boost to your trademark goodwill. So in this case, it's not human brains that store the reputation, but Google's search algorithm.

What about when you are a Taxi driver? The fact that people have your number stored in their address book under "taxi" is part of your goodwill as well.

In short, reputation is multi-faceted and inherently fuzzy. It can't be directly measured. If you tried you wouldn't even know where to start. Human brains? Google's search algorithm? All the pieces of paper with your telephone number in people's drawers?

But despite all its immeasurability we seem to be capable of safely storing the reputation in tokens such as trademarks.

But are we, really? A nice case study here is how MySQL database was sold to Sun Microsystems, Inc. and eventually ended being owned by Oracle Corporation. The first interesting part is that the code of the database was open source and so what was really sold was the goodwill associated with the name MySQL. The second interesting point is that original MySQL developers eventually forked the codebase and created a new database called MariaDB.

What we end up with is almost no difference in the product itself, but nice separation of goodwill associated with the MySQL name — which passed to Oracle — and goodwill associated with the identity of people who created the product — which went to MariaDB.

I am not qualified to do goodwill assessment in this case, but my guess would be that largest part of the goodwill want to Oracle and only a small part trickled down to MariaDB. In other words, a random investor would pay more for acquiring Oracle's MySQL trademark than for getting MariaDB trademark. (Anyone familiar with the matter, please do correct me if I am wrong here.)

If the above is true it means that trademarks make for pretty good containers of reputation. Even if a lot of other factors change, the goodwill mostly stays with the original trademark.

One may attribute this property to human inflexibility and limited ability to track all the details, i.e. failing to take into account that creators of MySQL went to work on MariaDB. However, I would argue that that's not the whole story. After all, Google's search algorithm exhibits exactly the same problem: If you search for MySQL you get result for, surprise, surprise, MySQL, not MariaDB.

As a conclusion let me summarize it like this: Reputation is scarce but not trasferrable. Reputation tokens are free, but they can be used to store reputation. They also happen to be transferrable.

Some examples:

Token

Reputation

Trademark

Goodwill

GitHub project

Stars, Followers

Twitter account

Followers

Webpage

Google page rank, Bing page rank

**Martin Sústrik, July 17th, 2017**