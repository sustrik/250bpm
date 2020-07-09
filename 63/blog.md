# Saving the journalism. With bitcoin.



We hear that journalism is dying every now and then. People are not willing to pay for news anymore. They expect to get them for free. If a journalist wants to live out of what they are doing they can either turn into an advertisement shop, virtually selling they readers to the advertisers or get gone. The problem is made much more grave by the fact that media is supposed to be one half of our democratic feedback loop.

Paywalls are often proposed as a solution. Fair enough, but I as a reader tend to just ignore the articles that are beyond a paywall. It's not that I am not willing to spend one cent to read the article, it's rather that the article is not worth enough for me to bother with figuring out how to pay and messing up with the credit card. And paying one cent by credit card feels just stupid. And so does paying for a long-term subscription given that I likely won't visit the site ever after.

However, I am willing to spend some CPU cycles to mine for Bitcoin and pass that to the publisher. The cycles would be wasted by ads anyway. So I don't really care. The only requirement is that it happens automatically and I am not inconvenienced by it.

Can it be done? What are the technical problems with offering such solution?

First thing that comes to mind is that Bitcoin payment takes approximately 10 minutes. 10 minutes later you have already forgotten that you wanted to read the article.

Second caveat is that you can't mine for arbitrarily small amount of cash. Wikipedia says that in 2012 the revard was 25 bitcoins per block. By now it's less, but still not the one cent you want to pay for reading the article.

Third problem has to do with ease of use: Typical user doesn't want to install a Bitcoin mining software to be able to read articles. They are willing to spend the CPU cycles, but not willing to do any annoying sysop work. They expect the site to take care of that for them.

And that's more or less it. It doesn't look so hard when put like this, does it?

And here's my solution:

1.  Publisher mines for bitcoins.
2.  They ask each reader to find a solution for an easier problem (less initial zeroes in the hash).
3.  Reader computes the hash and sends it back to the publisher.
4.  Publisher checks whether the hash is valid, and if so, displays the article.
5.  Most of the hashes publisher receives are worthless. However, once in a while the hash has enough initial zeroes to create a Bitcoin block.
6.  Profit!

See how it solves the problems outlined above:

First, there's no 10 min waiting interval. The initial exchange goes on between the publisher and the reader. Blockchain is not involved in any way. Thus, there are no hard limits on latency except for the time needed to compute the hash. And even that can be mitigated by displaying the first paragraph of the article immediately and computing the hash in the background. When the hash is ready, the rest of the article is displayed.

Second, the challenges sent to the readers are much smaller than mining a Bitcoin block. Publisher can scale them down to almost nothing. Theoretical lower limit is one initial zero in the hash, but in practice the lower limit is defined by the cost of interacting with the reader. If it takes more work than mining for Bitcoin yourself, it's not worth it.

Third, user doesn't have to install anything. Mining code is JavaScript sent to it by the publisher. Moreover, the communication is done via https ensuring that the hashes won't be stolen by third parties.

Some additional comments:

*   The journalism here can be replaced by any trade with similar economic characteristics. Are you a small death metal band? Want to make some cash by putting your stuff online? Here's the way to do it! Are you a fiction writer? Why not put your book online and monetise it on per-chapter basis?
*   Would readers abuse the system? Sending worthless hashes to the publisher, but keeping the winning ones for themselves? I don't think so. If one wanted to mine for Bitcoin they would be much better off doing it themselves. Making the publisher a gatekeeper for you access to the blockchain is nothing but a hurdle that makes the whole endeavour less profitable.
*   You may argue that JavaScript is a lousy way to do mining. I hear that JavaScript is pretty efficient these days but maybe you are right. Therefore, the hash computation should be done in a standardised way, so that browser/interpreter can at some point switch to doing the computation itself, in an optimised way, using native code.
*   Isn't it a nice startup idea? Do it as a service. Provide API for publishers so that they don't have to care about all the mining stuff themselves. Send them the mined cash monthly, ideally in USD, so that they won't even know that Bitcoin in involved. When you make your first million, buy me a beer.
*   Running the system as a shared service makes it interesting for small publishers. If you have just few views per day, it's going to take a long time till you are able to mine a Bitcoin block. It becomes more of a lottery. However, if a shared service distributes the cash to all publishers evenly (proportionally to the of number of views) it turns it a much better, predictable proposition.
*   Finally, it looks like the whole Bitcoin ecosystem could benefit by bringing much needed diversity to the mining pool. Eventually, one can imagine a world where people do Bitcoin transactions and at the same provide the CPU power to run the technology while accessing online content. The Bitcoin transaction fees are then passed to content creators on strictly vote-by-your-feet basis.

**September 15th, 2015**