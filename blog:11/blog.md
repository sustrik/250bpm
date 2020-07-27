# The Merit of AMQP (part I)



Couple of [AMQP](http://www.amqp.org)\-related blog posts have arrived lately. Reading it, I've realised that although I've been involved with AMQP from the very beginning I've never explicitly expressed my thoughts on it, on the split between AMQP/0-9-1 and AMQP/1-0 and related technical issues. Also, I believe that designing ZeroMQ gave me a pretty unique point of view on AMQP, that some of the readers may find interesting to explore.

8 Years in Making
=================

To start with, the goal of AMQP was breaking the IBM and TIBCO duopoly in enterprise messaging market and commoditisation of messaging middleware products. Both companies have charged exorbitant prices for the software and even wannabe competitor products were extremely costly. The idea was to define an interoperable messaging protocol and thus allow enterprises to switch messaging implementations without breaking the existing applications. Therefore, if incumbent vendor would go rogue with the licensing fees, the enterprise could smoothly migrate to a different vendor with more favourable pricing scheme.

By the time the work on AMQP have begun (2004) there was already an established API standard for enterprise messaging called Java Message Service, or [JMS](https://en.wikipedia.org/wiki/Java_Message_Service) for short. Of course, JMS works only with Java, but at least it defines a reasonable set of functionality to be supported by enterprise messaging product. Thus, the real challenge of AMQP was to define a wire protocol that could work as a communication medium between JMS clients and servers. And early versions of AMQP did just that. The protocol was basically reverse-engineered from JMS. You could browse through the specification and map AMQP concepts to JMS concepts in straightforward 1:1 manner. AMQP/0-9-1 standard (as used, for example, by RabbitMQ) is still very much JMS gone binary.

There's one digression to make here: The 1:1 mapping between JMS and AMQP/0-9-1 is somewhat obscured by replacement of JMS' Queue and Topic model with AMQP's Exchange-Binging-Queue model. The refactoring seemed to make sense at the time as it clearly separated the routing functionality (exchanges) from message queueing functionality (queues). From today's perspective though, I would say that Exchange-Binding-Queue model is rather a leakage of internal broker architecture (separate modules to route and queue messages) into the protocol. While the model allows for novel ways of interlinking different routing and queueing behaviours, in practice there are only two models that actually make sense: request/reply model embodied in JMS' "Queue" concept and publish/subscribe model modelled as "Topic" in JMS. All the additional flexibility provided by Exchange-Binding-Queue model is more or less good only for letting the user shoot himself in the foot.

Anyway, back to the story: By the end of 2007 I've started working on ZeroMQ. ZeroMQ had different goals from AMQP. Instead of trying to provide interoperability for traditional enterprise messaging (IBM WebSphereMQ and various copycat products) it rather tried to address the low-latency messaging market (TIBCO RendezVous, 29 West's LBM and alike) as well as messaging in 'common' rather than 'enterprise' scenarios. At first I've tried to use AMQP/0-9-1 model in ZeroMQ. I've even written a [whitepaper](http://www.zeromq.org/whitepapers:messaging-enabled-network) about it. However, AMQP never aligned well with the goals of ZeroMQ and I've finally dropped the AMQP support when releasing version 2.0 of ZeroMQ.

In 2008 AMQP/1-0 emerged. I was not much involved with AMQP working group by then so I have no idea why it have entirely dumped the previous versions of the protocol and sent all the work done by early adopters of the protocol down the drain.

The most puzzling aspect is that such a move seriously undermines the credibility of AMQP as a standard. After all, why should you invest in AMQP/1-0 if the working group is going to do the same thing next year, dump AMQP/1-0, publish completely unrelated AMQP/2-0 and make your investment worthless? It sounds counter-intuitive. Why would members of AMQP Working Group want to destroy the credibility of their standard?

There's one conspiration theory that comes to mind: Around the time AMQP/1-0 was first discussed, Microsoft joined the AMQP working group. By that time AMQP Working Group consisted of users of messaging technology (banks and alike) and few small messaging vendors. Red Hat was part of the group, but its Qpid product was relatively new, not established and have already strayed away from the original standard. RabbitMQ had an AMQP implementation, but back then it was not yet acquired by VMware and was thus a small and insignificant member of the group. Same applies to iMatix with its OpenAMQ implementation. Thus, the thinking of those in power in the Working Group may have been that credibility gained by getting established messaging vendor like Microsoft (DCOM, MSMQ, SOAP, WCF etc.) on board would compensate for the loss of credibility caused by ruining the investments made be early adopters.

The question, of course, is why not get Microsoft on board and preserve the standard at the same time. The answer seems quite obvious once you think of Microsoft joining the AMQP Working Group as of economic transaction. Microsoft offers credibility that goes with its membership in the standards group. The standard groups offers the "AMQP-compliant" stamp. Thus, to make the transaction acceptable by both parties, existing Microsoft products have to be stamped as "AMQP-compliant".

The facts seem to support the above explanation. Most importantly, the whole "broker model" part of the specification was dropped. AMQP doesn't define how the message broker should behave any more. It deals mostly with what happens on the wire between two TCP endpoints. As long as the bytes on wire are syntactically correct, broker is free to do anything and still be called AMQP-compliant. In practice it means the vendor can take an existing messaging product, implement a stand-alone well-encapsulated AMQP adaptor and there he goes without a need to re-write the whole product. If the broker model stayed in place, Microsoft would have to either create a new AMQP-compliant messaging technology or heavily re-factor its existing technologies. Both options are extremely expensive, not only in terms of the development cost, but primarily in the terms of credibility. New non-compatible product would dilute the credibility accumulated in the existing technologies. Refactoring existing deployed technologies means offending the customers. None of the two is acceptable, thus, AMQP standard has to be shoehorned to comply with existing Microsoft products.

The downside of dropping the broker model, of course, is that user can't rely on standardised semantics of the broker any more. Thus, if one AMQP-compliant broker implementation is replaced by another, the application will most likely break. The fact that original goals of AMQP project, interoperability and avoidance of vendor lock-in, are missing from the current official [statement of goals](http://amqp.org/product/solve) is in line with the above explanation.

Recently, I've seen couple of comments from Working Group members asserting that broker model is to be added to the specification in the future. Although there's no much point in discussing vapourware, there are three possible outcomes: First and most probably, the broker model never materialises. Second, the new broker model could be shoehorned to fit a particular Microsoft technology, say WCF. Third and least likely, if another big vendor, such as IBM, joins the group there's a non-zero chance that a normal standardisation process driven by multiple parties will emerge.

Anatomy of Messaging: Connection vs. Broker
===========================================

Having shortly reviewed the history of AMQP, let's now have a closer look at it from technical point of view.

If you look at any messaging protocol from 10,000 feet perspective, you'll almost always see two functionally distinct layers.

The lower one deals with what happens between exactly two TCP endpoints. It basically defines a "better TCP" to build the messaging solution on top of. This layer consists of features like initial handshaking, authentication, message delimitation, multiplexing, heartbeating etc.

Second layer deals with communication between more than two endpoints and is often referred to as "broker model" (although this is a misnomer: ZeroMQ implements this layer without a need for broker). Broker model defines the behaviour of queues shared between multiple connections as well as algorithms to route messages from clients to the shared queues and vice versa.

The following table may be of interest. I've compiled the list of better-known messaging standards and marked whether they deal with connection layer or the broker model layer:

|                                                                                         | Connection Layer | Broker Model |
| :-------------------------------------------------------------------------------------- | :--------------- | :----------- |
| [AMQP/0-9-1](http://www.amqp.org/specification/0-9-1/amqp-org-download)                 | Yes              | Yes          |
| [AMQP/1-0](http://www.amqp.org/resources/download)                                      | Yes              | No           |
| [ZeroMQ](http://www.zeromq.org)                                                         | No               | Yes          |
| [XMPP](http://xmpp.org/)                                                                | Yes              | Yes          |
| [MQTT](http://www.ibm.com/developerworks/webservices/library/ws-mqtt/index.html#N10084) | Yes              | Yes          |
| [STOMP](http://stomp.github.com/)                                                       | Yes              | No           |

Remark: ZeroMQ is a product and does not define a protocol. I've included it into the list as it is the only example of "broker model" running straight on top of raw TCP, with no intermediate "connection layer". (You may consider [this article](/concepts), where I've defined some basic concepts of distributed messaging, to be an initial step towards a formal protocol.)

Merit of AMQP/1-0
=================

To assess the merit of AMQP, it can't judged based on its original goals. With no broker model the goal of interoperability was not reached and we would have to write the protocol off as a failure. There would be nothing to blog about.

However, let's assume that the new goal (although not officially stated) is to standardise the connection layer ("better TCP") and that AMQP is thus a competitor to [SCTP](https://en.wikipedia.org/wiki/SCTP) rather then to full-blown messaging protocols like XMPP or MQTT.

From this point of view there are many technical questions to consider such as: How does AMQP deal with back-pressure? Does channelling work? What added benefit it brings over raw TCP? Is heartbeating defined is a versatile way or is it just a niche solution? What about reliability guarantees?

I would like to consider these questions in the next part(s) of this article.

**November 1st, 2012**
