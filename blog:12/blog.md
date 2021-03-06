# EINTR and What It Is Good For



EINTR is one of the POSIX errors that you can get from different blocking functions (send, recv, poll, sem\_wait etc.) The POSIX standard unhelpfully describes it as "Interrupted function." Googling for EINTR returns mainly random questions like "I am getting teh EINTR error. What now?" answered mostly by "Just restart the interrupted function."

None of this helps much when you want to correctly handle EINTR, actually understand what you are doing and why. In this blog post I'll try to explain what EINTR is good for and how to handle it in your code.

To understand the rationale behind EINTR, let's do a little coding exercise. Let's write a simple event loop that performs some action for every byte it receives from a socket. And let's pretend there's no EINTR and recv just continues waiting for data whatever happens:

    void event_loop (int sock)
    {
        while (1) {
            char buf [1];
            recv (sock, buf, 1, 0);
            printf ("perform an action\n");
        }
    }

The above program works great. However, interrupting the program using Ctrl+C kills it immediately, which may be a problem if we want to do some clean-up, for example, release some system-wide resources.

To handle Ctrl+C in a custom way we have to implement a signal handler:

    volatile int stop = 0;
    
    void handler (int)
    {
        stop = 1;
    }
    
    void event_loop (int sock)
    {
        signal (SIGINT, handler);
    
        while (1) {
            if (stop) {
                printf ("do cleanup\n");
                return;
            }
            char buf [1];
            recv (sock, buf, 1, 0);
            printf ("perform an action\n");
        }
    }

Ok. Looks good. What's the problem with that?

The problem is that recv is a blocking function. If Ctrl+C is pressed while the event loop is blocked in recv, you'll get a kind of deadlock: Signal handler is executed as expected, it sets 'stop' to 1, but then the execution blocks. The event loop is stuck in recv and has no opportunity to check whether 'stop' was set to 1.

The deadlock unblocks only when new data arrive via the socket. Then 'stop' is checked and the program exits decently. However, there's no guarantee that new data will arrive in a reasonable time, so pressing Ctrl+C may seem to have no effect. The program is probably going to terminate at some later point, but at the moment it's just stuck.

Enter EINTR.

POSIX specification defines that when signal (such as Ctrl+C) is caught, recv returns EINTR error. That allows the event loop to wrap over and check the 'stop' variable:

    volatile int stop = 0;
    
    void handler (int)
    {
        stop = 1;
    }
    
    void event_loop (int sock)
    {
        signal (SIGINT, handler);
    
        while (1) {
            if (stop) {
                printf ("do cleanup\n");
                return;
            }
            char buf [1];
            int rc = recv (sock, buf, 1, 0);
            if (rc == -1 && errno == EINTR)
                continue;
            printf ("perform an action\n");
        }
    }

The above code works more or less like expected. When you press Ctrl+C, program exits performing the clean-up beforehand.

EDIT: Please note that to make blocking fuctions like recv return EINTR you may have to use _sigaction()_ with SA\_RESTART set to zero instead of _signal()_ on some operating systems.

The morale of this story is that common advice to just restart the blocking function when EINTR is returned doesn't quite work:

    volatile int stop = 0;
    
    void handler (int)
    {
        stop = 1;
    }
    
    void event_loop (int sock)
    {
        signal (SIGINT, handler);
    
        while (1) {
            if (stop) {
                printf ("do cleanup\n");
                return;
            }
            char buf [1];
            while (1) {
                int rc = recv (sock, buf, 1, 0);
                if (rc == -1 && errno == EINTR)
                    continue;
                break;
            }
            printf ("perform an action\n");
        }
    }

When Ctrl+C is pressed in this case, signal handler is executed, 'stop' is set to 1, recv returns EINTR, but the program just calls recv again and blocks. 'stop' is thus not checked and the program gets stuck. Ouch.

Instead of remembering these intricacies you can just remember a simple rule of thumb: When handling EINTR error, check any conditions that may have been altered by signal handlers. Then restart the blocking function.

Additionally, If you are implementing a blocking function yourself, take care to return EINTR when you encounter a signal.

To give you a real world example of incorrectly implemented blocking function, here's a problem we encountered with ZeroMQ couple of years ago: Ctrl+C did not work when ZeroMQ library was used from Python (via _pyzmq_ language binding). After some investigation, it turned out that Python runtime works more or less like the examples above. If Ctrl+C signal is caught, it sets a variable in the handler and continues the execution until it gets to a point where signal-induced conditions are checked.

However, ZeroMQ library used to have a blocking recv function, that (oops!) haven't returned EINTR and rather ignored the signals.

What happened was that user called ZeroMQ's recv function from Python, which started waiting for incoming data. Then the user pressed Ctrl+C. Python's signal handler handled the signal by marking down that the process should be terminated as soon as possible. However, the execution was blocked inside ZeroMQ's recv function which never returned back to the Python runtime and thus the termination never happened.

Exiting the recv function with EINTR in case of signal solved the problem.

Finally there are few fine points to be aware of:

First, there's no EINTR on Windows. My assumption is that blocking functions cannot be combined with Ctrl+C and with decent clean-up on Windows. Maybe there's some esoteric API to handle this kind of situation, but I am personally not aware of it and I would be grateful for suggestions.

Second, even some POSIX blocking functions don't return EINTR in case of a signal. Specifically, this is the case for pthread\_cond\_wait and pthread\_mutex\_lock. pthread\_mutex\_lock is not often a problem as it is generally not used to block for arbitrary amount of time. Mutexes are normally locked only for a very short time until some simple atomic operation is performed. pthread\_cond\_wait is more of a problem. My suggestion would be to use sem\_wait (which returns EINTR) instead of pthread\_cond\_wait. Once again, if anybody knows how to perform clean shutdown when pthread\_cond\_wait gets into its way, let me know!

Third, even EINTR is not completely water-proof. Check the following code:

    volatile int stop = 0;
    
    void handler (int)
    {
        stop = 1;
    }
    
    void event_loop (int sock)
    {
        signal (SIGINT, handler);
    
        while (1) {
            if (stop) {
                printf ("do cleanup\n");
                return;
            }
    
            /*  What if signal handler is executed at this point? */
    
            char buf [1];
            int rc = recv (sock, buf, 1, 0);
            if (rc == -1 && errno == EINTR)
                continue;
            printf ("perform an action\n");
        }
    }

As can be seen, if the signal handler is executed after checking the 'stop' variable and before invoking the recv, the program will still be stuck. However, this is not a serious problem. For starters, the period between the check and the recv is extremely short and it is thus very unlikely that the signal handler gets executed precisely at that point. And even if that happens, pressing Ctrl+C for the second time sorts the problem out.

EDIT: It was suggested by Justin Cormack that _signalfd_ can be used to solve the last problem. However, keep in mind that first two problems remain: it doesn't work with Windows and it doesn't work with pthread\_cond\_wait. Moreover, it makes your program non-portable (works only on Linux). Finally, signalfd is not a good option when you are implementing a library. By using signalfd (or, for what it's worth, your own signal handler) you are messing with the signal handling algorithm of the main application. If, for example, the main application already has a signalfd handling Ctrl+C signal, creating a new signalfd in the library causes the signal to be delivered alternatively to the main application and to the library (first Ctrl+C is sent to the library, second one to the application, third to the library etc.) Which, of course, brings the problem back: You have to press Ctrl+C twice to exit the program.

EDIT: Ambroz Bizjak suggests to use pselect (and similar functions) to deal with the race condition above. The idea is that signals are blocked for a very short period of time before the blocking call. Once signals are blocked, the flags set by the handlers can be checked and pselect is called which unblocks the signals is an atomic manner. This trick is even applicable in libraries. If the library exposes a blocking function,you can extend it to expose a p\* variant of the function (for example, ZeroMQ could expose zmq\_precv in addition to zmq\_recv). User of the library can use this function to handle signals in a race-free way.

**November 5th, 2012**