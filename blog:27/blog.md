# Backdoors in Encryption Standards and How To Fight Them



In the last week there a lot of discussion of malevolent parties putting backdoors into encryption standards and how to prevent it. There have been a long thread at IETF mailing list about the topic (starting [here](http://www.ietf.org/mail-archive/web/ietf/current/msg82071.html)). NIST re-opened one of its standards due to worries that the backdoor was built in by NSA (see [here](http://csrc.nist.gov/publications/nistbul/itlbul2013_09_supplemental.pdf)). And so on.

It may happen that security agency walks into a standards body and demands that the backdoor is built in. That is a rather trivial case and it can be handled by adjusting the policy of the standard body accordingly. IETF, for example, did so in [RFC 2804](https://www.rfc-editor.org/rfc/rfc2804.txt).

That's not the real problem though. The real problem is when the standard is subverted silently, without anybody knowing about it.

As can be easily seen, the problem is not really technical in its nature. Spotting the backdoor can be extremely hard and the fact that the standard is public doesn't necessarily mean there is no backdoor built into it. The only real solution would be not to allow people with an incentive to build a backdoor into the standard anywhere near it.

That's, however, hard to achieve. FSB or NSA agents can act undercover, or they can bribe people already on the standard committees to push their agenda instead of them. To prevent that, the standard body would have to turn into a spy agency itself.

Fortunately, we already have entities that are good at the spying stuff (doing security screening, spotting infiltrators, holding people legally responsible if they defect etc.) And I would argue that we should use those entities rather than creating new ones. And yes, I am speaking about the security agencies themselves.

The idea is pretty straightforward: Take multiple encryption standards crafted by various mutually hostile entities (US, Russia, China, Iran, Cuba, North Korea) and use all of them to encrypt the data. That way, even if there is backdoor in each protocol, the only way to decrypt it would be for all those disparate players to cooperate. It would be like a vault with multiple keys possessed by different people.

One important point here is that whenever possible the standards should be crafted by closed entities such as NSA, FSB or China's Ministry of State Security. That gives us reasonable confidence that each encryption standard has exactly one backdoor. It's not likely that FSB succeeded to insert its own backdoor into NSA's standard or vice versa. If, on the other hand, we had used standards crafted by open organisations, say a W3C standard and an IETF standard, it's possible that NSA has backdoors in both of them and thus is able to decrypt the data singlehandedly.

Another important point is that the authors of individual standards should be as mutually hostile as possible. That prevents them to cooperate to decrypt any particular message. To increase the hostility couple of other organisations should be thrown into the mix. If, in addition to US, China and Iran, we'll encrypt the data by standards from FSF, Pirate Bay and WikiLeaks, we can be pretty sure that six of them will never agree on anything. Adding couple of standards created personally by well-known cryptographers, who have a lot of credibility to lose if it turns out they've deliberately built in a backdoor won't hurt either.

The final remaining problem, although unlikely to happen if the mutual hostility is well-balanced, is how to secure the communication if all the involved standard creators decide to cooperate. There are two possibilities here:

First, the security agencies may decide to share the backdoor each with another. However, if that happens, it would mean that NSA won't be able to protect its own communication from FSB and vice versa. Thus, both agencies would have to create a new, secret encryption standard for internal use. And if that happens, it takes a single leak to get the standard out to the public and at that point the leaked standard can be added to the encryption suite.

The second possibility is that the agencies won't share the backdoors, rather, they would decrypt data each for another ("spying as a service"). In such case, the order of encryption is important. The rule of the thumb is that the innermost level of encryption should not be the one created by the entity which threatens you the most, rather it should be the one crafted by its most direct enemy. That way we ensure that by decrypting data for others, you are basically cooperating on hurting yourself. After all, the one who will get the plaintext first is your most direct enemy. For example, if the files leaked by Snowden were encrypted in this way and if FSB asked NSA to decrypt it's part of the suite, NSA won't get any information, it wouldn't even know what it is decrypting, but in the end it would help WikiLeaks to get the files (assuming that WikiLeaks' encryption standard was used as the innermost one).

**September 11th, 2013**