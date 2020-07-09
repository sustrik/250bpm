# Implementing Network Protocols in User Space



Implementing network protocols in user space is not as uncommon as it may seem. The advantages when compared to implementing them in the kernel space range from easier development, more freedom to experiment and greater portability to less hassle with the distribution (the pain of getting the patch into the mainline kernel vs. simply uploading a user space library to GitHub), improved performance thanks to kernel by-pass and no way to provide a kernel space implementation for proprietary platforms like Windows.

While my experience in the area is based on my work on [ZeroMQ](http://www.zeromq.org) and more recently on [nanomsg](http://nanomsg.org), there are many other libraries that share the same challenge. One may mention, for example, [OpenPGM](https://code.google.com/p/openpgm) (reliable multicast, RFC 3208), [UDT](http://udt.sourceforge.net/) (bulk transfer protocol) or [OpenOnload](http://www.openonload.org/) (Solarflare's kernel by-pass networking).

This article gives an overview of technical challenges of designing an idiomatic APIs for network protocols implemented in user space and provides a background for my recent [EFD\_MASK patch to Linux kernel](https://lkml.org/lkml/2013/2/8/67).

When implementing a network protocol in user space you will almost certainly start with some kind of clone of BSD sockets API:

    struct myproto_sock {
        ...
    };
    
    struct myproto_addr {
        ...
    };
    
    struct myproto_sock *myproto_socket (void);
    int myproto_close (struct myproto_sock *s);
    int myproto_bind (struct myproto_sock *s, myproto_addr *addr);
    int myproto_connect (struct myproto_sock *s, myproto_addr *addr);
    ssize_t myproto_send (struct myproto_sock *s,
        const void *buf, size_t len, int flags);
    ssize_t myproto_recv (struct myproto_sock *s,
        void *buf, size_t len, int flags);

However, when implementing anything except for the simplest client applications this API is not sufficient. To handle more than one socket in parallel, you need polling. For example, your server application may want to wait until at least one of several myproto sockets becomes readable.

Once again, the most obvious solution is to fork the polling API from BSD sockets:

    struct myproto_pollfd {
        struct myproto_sock *fd;
        short events;
        short revents;
    };
    
    int myproto_poll (struct myproto_pollfd *fds, nfds_t nfds, int timeout);

The next stumbling block is combining classic TCP or UDP sockets with myproto sockets in a single pollset. What if the server application wants to handle a set of myproto sockets along with a set of TCP sockets? The above API doesn't support that kind of thing. We have to modify the myproto\_pollfd prototype to allow for using either myproto\_sock pointer or regular OS-level file descriptor:

    /*  rawfd field is used instead of fd when the latter is set to NULL */
    struct myproto_pollfd {
        struct myproto_sock *fd;
        int rawfd;
        short events;
        short revents;
    };

The API is getting a little ugly, but it's still more or less usable. Unfortunately, it's not yet the end of the trouble. Actually, this is the point where things start to get hairy. Let's inspect the next use case.

There are many widely used asynchronous networking frameworks out there. Their main goal is to shield the user from the complexity of handling many connections in parallel. Obviously, central piece of each such framework is a loop polling on a set of sockets and invoking user-supplied handlers when the poll reports a network event. The polling itself is done via one of the system-level polling mechanisms, such as select, poll, epoll, kqueue, IOCP, or /dev/poll.

However, myproto sockets require a special polling function (myproto\_poll) and thus cannot be integrated with such frameworks.

In theory, the framework can be modified to use myproto\_poll instead of the system poll, but such a patch is never going to get into the mainline. The most obvious reason is that it makes the framework dependent on the myproto library, but the real problem occurs when there's a need to handle two different user space protocols. One asks the framework to use myproto\_poll function, other one asks it to use someoneelsesproto\_poll. There's no way to reconcile the two.

In short, protocol developer's only option is to somehow provide a native file descriptor for the frameworks to poll on. It can be done, for example, in the following way. This example assumes that myproto is a protocol built directly on top of IP layer:

    struct myproto_fd {
        int raw; /*  underlying IP (SOCK_RAW) socket */
        ...
    };
    
    int myproto_getfd (struct myproto_fd *s)
    {
        return s->raw;
    }

The user is expected to retrieve the underlying system file descriptor from myproto\_fd (via myproto\_getfd function) and use it for actual polling (select, poll, epoll etc.)

The problem with this approach is that the underlying file descriptor signals individual poll events depending on what's happening on IP layer, rather than on the myproto layer. For example, if a myproto control packet with no embedded user data arrives, the file descriptor will signal POLLIN, however, subsequent myproto\_recv will return no data.

To solve this problem we have to implement a new function that will check whether the socket is **really** readable. Something like this:

    struct myproto_fd {
        int raw; /*  underlying IP (SOCK_RAW) socket */
        uint8_t rx_buffer [128 * 1024]; /* receive buffer */
        size_t bytes_in_rx_buffer; /* amount of user data in reveive buffer */
        ...
    };
    
    int myproto_getfd (struct myproto_fd *s)
    {
        return s->raw;
    }
    
    int myproto_can_recv (struct my_proto_fd *s)
    {
        if (s->bytes_in_rx_buffer > 0)
            return 1;
        else
            return 0;
    }

The intended usage is as follows:

1.  Retrieve the raw file descriptor form myproto socket.
2.  Poll on it.
3.  When POLLIN is signaled, use myproto\_can\_recv to find out whether the socket is really readable.
4.  If so, receive the data via myproto\_recv. The call is now guaranteed to return at least 1 byte.

That's already pretty ugly. In the real world the API tends to get even worse. There are multiple reasons for that: The need to report special conditions like POLLERR, POLLPRI or POLLHUP. Using multiple underlying raw sockets. Handling underlying raw sockets in a background thread. Etc.

Let's consider the example of ZeroMQ. With ZeroMQ underlying sockets are managed by a worker thread. Worker thread communicates with user thread by sending it events via a socketpair. One event may mean, for example, "new messages have arrived". However, for efficiency reasons the event is not sent for every single arrived message, only when there was no message in the rx buffer beforehand. This kind of approach is called edge-triggering.

So, when user thread wants to poll on ZeroMQ socket it retrieves its internal file descriptor (receive side of the socketpair) and uses it for polling. Given that it is edge triggered, user has to deal with edge-triggering in the application. And it turns out that edge triggering is very counter-intuitive for most users and that it is seen as adding significant complexity to the API and leading to subtle bugs in the applications.

If you want to have a closer look at the convoluted API, check documentation for zmq\_poll as well as for ZMQ\_FD and ZMQ\_EVENTS socket options. OpenPGM gets into pretty similar situation — see PGM\_SEND\_SOCK, PGM\_RECV\_SOCK, PGM\_PENDING\_SOCK and PGM\_REPAIR\_SOCK socket options. UDT implementation, if I recall correctly, just gives up and doesn't provide any generic polling mechanism at all. OpenOnload, on the other hand, hijacks the whole system socket API and replaces it with its own implementation.

As can be seen, all the possible solutions are basically ugly hacks. The question thus is, what can be done to fix the problem in a systematic manner.

Here's where proposed EFD\_MASK patch for Linux kernel kicks in.

The fundamental idea is that it should be possible to create a system-level file descriptor to work as a placeholder for a socket implemented in the user space. Additionally, user space should be able to specify which events will be returned when the descriptor is polled on.

And as it turns out, Linux already offers an object that almost fits the bill. It's called eventfd.

For those not familiar with eventfd, it is basically a counter. By writing data to the eventfd you increase the counter, by reading data from eventfd you decrease the counter. When you poll on eventfd, it signals POLLIN when counter contains a value greater than zero. POLLOUT is signaled all the time except for the case when the counter reaches value of 0xffffffffffffffff.

There are couple of things missing though:

1.  There's no way to associate user space data (socket state) with eventfd.
2.  While eventfd is great for signaling POLLIN and more or less viable for signaling POLLOUT, you can't force it to signal special events, such as POLLHUP or POLLPRI.
3.  You can't even make it signal all possible combinations of POLLIN and POLLOUT. Specifically, there's no way to signal neither POLLIN nor POLLOUT, which is pretty common condition that can occur quite easily in network protocols (when receive buffer is empty and send buffer is full).

To solve these problems we need to, first, associate an opaque pointer with the eventfd, and second, replace eventfd's counter semantics with mask semantics, i.e. network protocol implementation should be able to explicitly specify the mask of events to be signaled when the file descriptor is polled on.

At the moment, the addition to the existing Linux eventfd API looks like this:

    #define EFD_MASK 2
    
    struct efd_mask {
        uint32_t events;
        union {
            void *ptr;
            uint32_t u32;
            uint64_t u64;
        };
    } __attribute__ ((__packed__));

You can use **eventfd** system call in combination with EFD\_MASK flag to create a special type of eventfd object with mask semantics:

    s = eventfd (0, EFD_MASK);

You can use **write** system call to set events and opaque data to the eventfd:

    struct efd_mask mask;
    mask.events = POLLIN | POLLHUP;
    mask.u32 = 1234;
    write (s, &mask, sizeof (mask));

Afterwards, you can use **read** system call to get currently set events and opaque data from the eventfd:

    struct efd_mask mask;
    read (s, &mask, sizeof (mask));
    assert (mask.u32 == 1234);

Finally, when you poll on the eventfd using **select**, **poll** or **epoll\_wait** function, you'll get the events specified by last events written to eventfd:

    struct pollfd pfd;
    pfd.fd = s;
    pfd.events = POLLIN | POLLOUT;
    int cnt = poll (&pfd, 1, -1);
    assert (cnt == 1);
    assert (pfd.revents == POLLIN | POLLHUP);

What follows is an example on a network protocol implemented in user space. It takes advantage of EFD\_MASK functionality to provide socket-like behaviour to the user. There's are only three functions (opening socket, closing socket and receive) in the example. Other functions (send, setsockopt, connect, bind etc.) are left as an exercise for the reader:

    struct myproto_state
    {
         /*  Undelying raw sockets go here, protocol state machine etc. */
    };
    
    int myproto_socket (void)
    {
        int s;
        struct myproto_state *state;
        struct efd_mask mask;
    
        /*  Create the file descriptor to represent the new myproto socket. */
        s = eventfd (0, EFD_MASK);
    
        /*  Create socket state and associate it with eventfd. */
        state = malloc (sizeof (struct myproto_state));
        mask.events = 0;
        mask.ptr = state;
        write (s, &mask, sizeof (mask));
    
        return s;
    }
    
    int myproto_close (int s)
    {
        struct efd_mask mask;
        struct myproto_state *state;
    
        /*  Retrieve the state. */
        read (s, &mask, sizeof (mask));
        state = mask.ptr;
    
        /*  Deallocate the state and close the eventfd. */
        free (state);
        close (s);
    
        return 0;
    }
    
    ssize_t myproto_recv (int s, void *buf, size_t len, int flags)
    {
        struct efd_mask mask;
        struct myproto_state *state;
    
        /*  Retrieve the state. */
        read (s, &mask, sizeof (mask));
        state = mask.ptr;
    
        ... move data from protocol's rx buffer to the user's buffer ...
    
        /*  If there are no more data in rx buffer, unsignal POLLIN. */
        if (state->rx_buffer_size == 0)
            mask.events &= ~POLLIN;
    
        /*  Store the modified poll flags. */
        write (s, &mask, sizeof (mask));
    
        return nbytes;
    }

The code is relatively self-explanatory, so let me make one final remark. All the socket functions (except for socket creation and termination) follow the same pattern:

1.  Read from eventfd to get the socket state
2.  Do actual work. Modify the poll flags in the process, if needed.
3.  Write the state to the eventfd.

Following these instructions should make implementing network protocols in user space easy. Or, if not easy (network protocols rarely are) it at least allows developers to focus on the functionality of the protocol rather than force them to fight with constraints and deficiencies of the underlying operating system.

**February 8th, 2013**