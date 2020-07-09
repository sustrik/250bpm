# TCP and heartbeats



Heartbeating is a common technique to check whether network connection is alive. The idea is that each end of the connection sends small packet od data called "hearetbeat" once in a while. If the peer doesn't receive a heartbeat for some time (typically a multiply of the interval between the heartbeats), the connection is considered broken.

Interestingly, TCP protocol doesn't provide heartbeats (there are optional keep-alives that are operating on scale of hours, but these are not really useful for swift dectection of network disruption). In short, if network connection is broken, TCP endpoints are not notified about the fact.

The problem is mitigated by the fact that if the application at the endpoint terminates or crashes, the peer is notified via FIN or RST packet and is thus aware of the connection failure. Therefore, you are going to experience the problem of missing failure notification only if the network itself is broken, e.g. if your router crashes, cable is cut, your ISP experiences a failure etc. In such case the TCP endpoint will live on forever, trying to communicate with the inaccessible peer.

For many applications, e.g. web browsers, this kind of behaviour makes sense. If the user feels the browser is stuck he can just hit the "reload" button. The browser will then try to open a new TCP connection. The attempt at the initial TCP handshake fails and user gets notified about the fact.

For other kind of applications — specifically those with high-availability requirements — the missing failure notification is a big deal. Imagine a critical application that has redundant access points to the network, for example via two different ISPs. The idea is to use one of the providers and fall back to the other one only if the first one becomes unaccessible. The idea is nice, but there's a catch: If TCP implementation doesn't let you know that the peer is inaccessible you have no reason to switch to the fall-back provider. You will continue using the failed provider, possibly missing some critical data.

That's why critical applications as well as tools intended to build such critical applications (e.g. message queuing systems) re-implement heartbeating on top of TCP over and over again. This article tries to explain the problems encountered when doing so.

Typically, business data (messages) are mixed with heartbeats within a single TCP bytestream. The main concern is thus to prevent one messing with the other. In other words, heartbeats shouldn't disrupt data transfer and data transfer should not cause hertbeating to misbehave, for example by reporting false connection failures or, coversely, not reporting actual connection failures.

The problem hits once the application stops reading data from the TCP connection. The heartbeats may be arriving, however, they cannot be read, because there are messages stuck in TCP receive buffer in front of them. Given that TCP doesn't provide a way to read data from the middle of the receive buffer, the application has no idea whether the heartbeats are arriving or not.

![heartbeats1.png](http://www.250bpm.com/local--files/blog:22/heartbeats1.png)

It's not immediately visible whether this is an actual problem or whether it can be solved by some clever trick. To get better understanding, consider the following questions and answers:

Q: Well, we can read those obnoxious business data, store it in a memory for a while and check whether heartbeats are still arriving, right?

A: The problem with that is that the application may be not reading data for a long time. For example, it may be processing some complex and lengthy task and ignore incoming messages while doing so. Or it may be waiting for user input and the user went out for luch. Whatever the reason, in the meantime all the data from the TCP connection have to be read to memory to be able to check whether heartbeats are arriving as expected. So, if there's a lot of incoming data, the application is ultimately going to exhaust all available memory and get killed by the operating system.

Q: A-ha! That's what we have message brokers for. They are supposed to have a big disk space available, and can store large amount of data without failing. Thus, if have a message broker in the middle, we are safe, no?

A: The problem is that heartbeats should flow in both ways. Even if message broker is able to deal with large amounts of data to store, the client application has to do the same thing to make sure that it receives heartbeats from the broker. And given that application is likely to run on a modest desktop, on a mobile phone or on a blade server with no local disk space, the memory is going to be exhausted pretty quickly.

Q: OK, but wait a second! If application is not receiving the data at the moment we don't care whether network failure is detected straight away. It should be sufficient to detect the failure once the application starts receiving data again and do all the failure handling, such as falling back to a different ISP, at that time.

A: Unfortunately, no. Imagine you want to send data instead of receiving them. In such case you won't detect the connection failure because you are not reading the data, including potential heartbeats, from the connection. Consequently, you will send the data to a broken connection. The data are not going to be delivered and — even worse — you are not going to be notified about the fact!

Taking the previous Q&A into account, there's only one way to deal with the problem: Preallocate a buffer at the endpoint to store any outstanding inbound data and introduce some kind of flow control to make sure that the buffer is never over-flowed. For example:

1.  Preallocate 100 bytes of buffer.
2.  Send a control message to the peer letting it know there are 100 free bytes that can be filled in.
3.  Peer gets the control message and it knows it can send at most 100 bytes.
4.  Say it has 30 bytes of data to send. So it sends them and it is aware of the fact that it can still send 70 more bytes, if needed.
5.  User reads 20 of the 30 received bytes. That leaves 90 bytes in the buffer free to be used.
6.  User sends a control message to the peer letting it know there are 20 more bytes avialable.
7.  The peer gets the control message and adds the new bytes to its current credit. Now it knows it can send 90 bytes (70+20=90).
8.  Etc.

This kind of alorithm ensures that there are no intervening data in TCP buffers that would prevent heartbeats to be passed through the connection without being stuck in the middle.

Thus, when you are evaluating a solution that implements heartbeating on top of TCP here is a checklist to help you to find out whether it actually works:

*   If there are heartbeats but there's no flow control, the solution won't work.
*   There must be a way to split larger messages into smaller units that will fit into the preallocated buffer. If there's no such mechanism, the solution won't work.
*   The credit in the flow-control mechanism must be expressed in terms of bytes, not messages. If it uses number of messages to control the flow, the solution won't work.
*   If the protocol allows to issue more credit than the space available in the receive buffer, the solution won't work.

The above being said, there is one subtler aspect of the problem, an aspect that hints at a more general problem with Internet stack itself.

In the case of heartbeats on top of TCP as well as in the case of multiplexing on top of TCP (read the related article [here](/blog:18)), one has to re-implement a big part of TCP (windowing and flow control) on top of TCP proper. It sounds almost like an engineering anti-pattern. The functionality should not be copy-pasted among the layers of the stack, rather, it should be localised at one well-defined layer. For example, routing is implemented by network layer. End-to-end relaibility is implemented by transport layer. And so on. However, what we are getting here is the same feature implemented redundantly at various layers of the stack.

Obviously, the right solution would be implement a new transport protocol directly on top of IP protocol, one that would provide desired functionality — failure detection and/or multiplexing — directly, without duplicating the features.

And, as a matter of fact, the above was already done. The protocol built directly on top of IP with both heartbeating and multiplexing is called [SCTP](https://en.wikipedia.org/wiki/SCTP) and is available out of the box in most operating systems.

And here comes the problem: SCTP is not used, even for projects where those features are needed. Instead, they are lousily re-implemented on top of TCP over and over again.

What's going on here?

I mean, SCTP has all features necessary for networking business-critical applications. By now, 13 years since its standardisation, it should be used almost exclusively by banks and such.

Except that it's not.

What happens is that developers are not aware of SCTP. That admins are not fond of having non-TCP packets on the network. That firewalls are often configured to discard anything other than TCP or UDP. That NAT solutions sold by various vendors are not designed to work with SCTP. And so on, and so on.

In short, although designers of the Internet cleverly split the network layer (IP) from transport layer (TCP/UDP) to allow different transports for users with different QoS requirements, in reality — propelled by actions of multitude of a-bit-less-clever developers — the Internet stack have gradually fossilised, until, by now, there is no realistic chance of any new L4 protocol gaining considerable traction.

The process of fossilisation of the Internet stack seems to proceed even further. Gradually, HTTP traffic is becoming dominant (consider, for example, moving from traditional SMTP-based emailing to gmail) and at some point it can possibly turn any non-HTTP protocol into persona non grata in the Internet world.

Even further: With advance of WebSockets we now have a full-blown transport protocol, an equivalent to TCP, on top of HTTP!

And it's unlikely that that will be the end of the story.

So, while re-implementing TCP functionality on top of TCP may seem like a silly engineering solution when you look at it with narrow mindset, once you accept that Internet stack is formed by layers of gradually fossilising protocols, it may actually be the correct solution, one that takes political reality into consideration as well as technical details.

And hopefully, at some point, when everbody have already migrated to some future TCP-on-top-of-TCP-on-top-of-TCP-on-top-of-TCP-on-top-of-TCP protocol, we can create a shotcut and get rid of those good-for-nothing intermediate layers.

**April 24th, 2013**