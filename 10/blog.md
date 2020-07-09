# Getting Rid of Domain Registrars Using Bitcoin Algorithm



Recently I've stumbled upon an though-provoking article [here](http://paulbohm.com/articles/bitcoins-value-is-decentralization). What it says is that whatever the benefits of Bitcoin as a distributed currency, the biggest deal is that it provided us with a viable algorithm for reaching consensus in highly distributed global-scale systems. I would also say that actually _proving_ that the algorithm works on global scale in real world is a great and almost unprecedented feat.

The article goes on to hint that the Bitcoin algorithm may be used to fully decentralise domain name system, which sounds like a great idea. As a mental exercise, let's now explore possible implementation and social dynamics of such a system.

Currently, domain names are stored in distributed database called DNS. The domain namespace is split in hierarchical manner and managed by different organisations like ICANN, national domain registrars etc.

The idea of Bitcoin-like domain name system, on the other hand, is that there is no central authority for assigning domain names. Rather, domain names are assigned by distributed consensus, similar to how bitcoins are assigned to individual owners. Bitcoin algorithm is able to prevent double spending (using same Bitcoin to pay twice) and in the same way the domain name system should be able to prevent assigning the same domain name to two different owners.

In other words, imagine that rather than buying your domain name from the central authority you would be able to "mine" it. By spending non-trivial amount of CPU time the domain name would be assigned to you and will become unavailable for others. You would simply download a mining program, enter the domain name you wish to use and let it work for say 24 hours. Next day, you'll have a key to the domain.

The key would entitle you to pair your domain name with an IP address, sign it and publish it. Everyone would be able to independently check whether the name-address pair was signed by the rightful owner of the domain or whether it is a fake.

Now let's think about social dynamics of such system.

First, it solves some real problems:

1.  It would make domain names a real property, not just a temporary license acquired for one year or such.
2.  There would be no gatekeepers, like national registrars, who could deny you the domain name, force you through annoying bureaucratic process or ask for expensive registration fees (gTLDs are one a $185,000!)
3.  There would be no way to track down the owner of the domain via credit card number used to pay the registrar. In fact, there would be no such payment.
4.  There would be no way to hijack domain name (domain seizures, censorship etc.) Infrastructure would be able to distinguish fake domain name entries, interpret them as domain name resolution failures and try to route around them. A court or a political leader won't be able to _disappear_ a domain.

The above means that there's a real value in implementing such a system. The next question is where there is a viable path for gradually migrating existing infrastructure to the new domain system without disrupting the old one (think pf IPv6 deployment problem).

What's needed for successful establishment of the new system is, first, extremely low cost of entry and, second, a motivation to do so even though the system is not widely used yet.

The low cost of entry is the problem IPv6 is struggling with. Deploying IPv6 means that all the old hardware should be be replaced, which is extremely expensive. As for the new domain name system, we could address large portion of the traffic (namely web traffic) using a very simple means with no change to infrastructure whatsoever and thus almost no associated cost.

All that's needed is a web service (or, preferably, several of them) that would resolve a new domain name and redirect the browser to the appropriate IP address. For example, following URL

    http://www.dns-resolver.org/my-new-domain-name/web-page.html

could redirect the browser to

    http://212.34.77.115/web-page.html

As can be seen there's zero cost for both owner of the domain and for the web-browsing individual. The only cost is in running the resolver service.

Once there are enough websites using the new domain name system, the rest of the infrastructure can be gradually adjusted to support it natively (adding new record types to DNS, enabling non-web-based applications to use new domain names etc.)

The other requirement for successful launch of new domain name system is motivating the early adopters. Fortunately, domain name system seems to have strong inherent motivation for early adoption, as we've seen with introduction of .xxx domains and custom gTLDs. Opening a new namespace results in a "gold rush" where everybody tries to grab the best domain names before everyone else is able to. The fact that the new domain name system has no regulation, no central authority to appeal to and that the domain names are granted for perpetuity makes the urge for rapid land grab even stronger. The nice thing is that people are motivated to grab the domain names even if they don't believe in viability of the new system. They should get the domain names just in case. Imagine what hell of a situation it would be if 'google' domain was owned by Apple or vice versa!

One concern here is that domain squatters may be the first to grab the lucrative domain names and thus cause real companies boycott the whole new naming system. To prevent this problem the algorithm may be shaped in such a way that the shortest domain names would be the most expensive to "mine". For example, while mining for a 10-letter domain name could take 24 hours of CPU time, mining for a 3-letter domain name could take several years.

In conclusion, it looks like implementing a fully decentralised domain name system free of any form of corporate and/or government control is a viable endeavour (what's needed is a couple of programmers and moderate amount of money) and chances of it getting traction and being widely adopted are good. There are some interesting unresolved problems, like handling compromised domain names (key is leaked) and dead domain names (key is lost), but these are in no way show-stoppers and can be resolved as we go.

**Martin Sústrik, October 17th, 2012**