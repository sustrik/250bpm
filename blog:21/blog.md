# How to Write a Language Binding for nanomsg

Language bindings are pieces of infrastructure that allow nanomsg to be used from different programming languages. This article is meant to provide some hints that may be helpful for binding developers.

Reusing ZeroMQ bindings
=======================

The easiest way to access nanomsg from various languages would be to simply reuse [ZeroMQ language bindings](http://www.zeromq.org/bindings:_start) (there are approximately 40 of them at the moment). To help with that, nanomsg provides a ZeroMQ compatibility mode which produces a fake ZeroMQ library that simply forwards the function invocations to nanomsg.

    $ mkdir build
    $ cd build
    $ cmake -DZMQ_COMPAT=ON ..
    $ make
    $ sudo make install

Although the library is fully ABI-compatible with ZeroMQ, there are differences in functionality between two libraries — nanomsg provides more messaging patterns etc.

Of course, original ZeroMQ bindings are not aware of the new functionality and lack definitions for the new constants. Thus, the user has to enter the constants by their numeric values. For details have a look at [nn\_zmq(7)](http://nanomsg.org/v0.0.0/nn_zmq.7.html) manual page. However, if the language binding uses enums instead of ints for socket types, socket options etc., there's little the user can do to access the new nanomsg functionality. The binding won't just allow unknown constants to be passed to the functions.

Forking ZeroMQ bindings
=======================

The above discussion indicates that using native ZeroMQ bindings with nanomsg's ZeroMQ compatibility mode is pretty rough and unreliable way for accessing the library.

The alternative is, of course, to build a native nanomsg binding. And the easiest way to do that, given that API/ABI of ZeroMQ and nanomsg are very similar is to fork the existing ZeroMQ binding and convert it into nanomsg binding.

When doing so, you should be careful about the license. While nanomsg is licensed under MIT which allows it to be combined with any other possible license (you can, for example, close source and sell the binding), the license of the original ZeroMQ binding may be more restrictive. For example, if the ZeroMQ binding is licensed under LGPL, the derived nanomsg binding has to be licensed under LGPL as well.

Also, don't stop reading here and check the comments below about writing a new nanomsg language binding. Some of those may prove useful even when converting existing ZeroMQ binding to use nanomsg.

Writing a new binding
=====================

Plug-ins vs. native code
------------------------

There are two broad categories of language bindings. Some languages allow you to implement a binary module (in most cases written in C) that is then loaded and used by the language runtime. This is the case, for example, of Java JNI. Other languages provide a way to define the library's ABI in language-specific way. This definition then allows the nanomsg functions to be accessed directly from the language. This is the case of, for example, Ruby FFI. Quite a few languages allow for both approaches. In such case it is important to understand that they are not necessarily equivalent in terms of performance and you should take that into account when deciding on the implementation strategy. For example, one experiment done in the past (performed by Gonzalo Diethelm) showed that Java binding based on JNI is much faster than one based on JNA.

Plug-ins
--------

Plug-ins are simply shared libraries that provide an API to interface with the language runtime.

Given that almost all such plug-ins are written in C, the implementation of the plug-in has access to all the symbols defined in nanomsg C header files.

One particular symbol that is of interest is NN\_VERSION. It is a macro indicating the current version of the library. It allows the binding to be compiled with different versions of nanomsg. Imagine that new function nn\_foo() is added to nanomsg in version 1.2.3. When support for this function is it added to the binding, it should be activated only for version equal to or higher than 1.2.3, this way:

    #if NN_VERSION >= NN_MAKE_VERSION(1,2,3)
    /*  Implement wrapper for nn_foo() here. */
    #endif

While some languages may require the constants (such as NN\_PUB or NN\_SNDBUF) to be available at the compile time, other languages may permit populating the set of constants in run-time. The latter is the preferred option as it allows binding to remain unchanged even if the library evolves and defines new constants. For details of implementing the runtime retrieval of constants see the dedicated section below.

Native code
-----------

Some languages allow to define and use the library ABI in a native way. Say, with Lua FFI (by Evan Wies and Pierre Chapuis), nn\_socket() function is defined like this:

    ffi.cdef([[
        int nn_socket (int domain, int protocol);
    ]])

While the fact that there's no need for additional binary component is nice, the obvious problem with this approach is versioning. If there happens to be an old nanomsg library installed on a box, the newer binding may attempt to access non-existent symbols.

To take care of this, binding should use nn\_symbol() function to retreive the version info (NN\_VERSION) constant and check whether the library isn't older than expected. Alternatively, binding may decide to support multiple versions of nanomsg and decently downgrade the functionality if an old version of library is encountered.

Run-time retrieval of constants
-------------------------------

If the language allows to define new constants in the runtime, binding should prefer doing it that way to copy-pasting all the constants from nanomsg header files to the binding. That way, if set of constants in main nanomsg library changes (e.g. by adding a new socket option) the binding will still work without a need to be modified or re-built.

To retrieve the constants in run-time, use [nn\_symbol()](http://nanomsg.org/v0.0.0/nn_symbol.3.html) function. Here is how it's done by Ruby binding (implemented by Chuck Remes):

      index = 0
      while true
        value = FFI::MemoryPointer.new(:int)
        constant_string = LibNanomsg.nn_symbol(index, value)
        break if constant_string.nil?
        const_set(constant_string, value.read_int)
        index += 1
      end

Managing socket lifetime
------------------------

While nanomsg API provides functions for creating and closing sockets (nn\_socket and nn\_close respectively), object-oriented language may prefer to implement socket as an object and call nn\_close() function from the destructor.

If so, it's important to consider that nn\_close() is a blocking function — it may wait for period specified by NN\_LINGER socket option while any pending outbound data are sent. If blocking in destructor would cause serious problems to the language runtime, such as entirely blocking the garbage collection process, you should consider exposing nn\_close() function directly to the user.

Sending and receiving messages
------------------------------

Wrapping most nanomsg functions is pretty straightforward. Special care, however, should be taken of nn\_send and nn\_recv.

These functions deal with messages. Message, from the point of view of nanomsg, is an uninterpreted binary BLOB, in other words, just an arbitrarily long sequence of bytes. The binding should decide how to represent such an object in the native language. For example, in some languages, the "string" type may not be the right option as the strings can only be used to store text in UTF-8 format. In most cases the language does have a datatype suitable for representing a BLOB. If that's not the case, the last resort solution is to represent messages as strings containing Base64-encoded binary data.

nn\_sendmsg() and nn\_recvmsg() functions provide an option to use C gather/scatter arrays (passing data in several non-continuous memory chunks). Many languages don't have a native concept of gather/scatter or, for what it's worth, of a memory buffer. Trying to expose this functionality in such languages doesn't make sense. Instead, send/recv functions should deal with exactly one message at a time.

Finally, receiving a message into preallocated buffer — as done by nn\_recv() function — doesn't make sense in many languages. Instead, the binding implementation should use nn\_recv in combination with NN\_MSG flag to get a buffer allocated by nanomsg library, then copy the buffer into native object and finally deallocate the buffer returned by nn\_recv(). Here's an example of such implementation:

    object *recv (int s, int flags)
    {
        int rc;
        void *buf;
        object *msg;
    
        rc = nn_recv (s, &buf, NN_MSG, flags);
        msg = create_object ("BLOB");
        memcpy (getbuffer (object), buf, rc);
        nn_freemsg (buf);
        return msg;
    }

Zero-copy
---------

The rule of thumb with zero-copy is: If you don't need it and/or don't fully understand how it works, just don't do it.

Zero-copy means that the application has to deal directly with different native memory buffers, for example with blocks of shared memory, or memory pinned down to physical memory address (so as to be accessible by zero-copy CPU-bypass techniques) and so on. This is hard, and sometimes even impossible, to get working with languages with automatic garbage collection.

If you still want to provide zero-copy, make sure to discuss it on the nanomsg mailing list or IRC channel in advance to avoid possible pitfalls.

Error codes
-----------

nanomsg uses POSIX error codes to indicate errors (EINVAL, EMFILE etc.)

While numeric values of these errors may be available in the native language, they are also provided by nn\_symbol() function.

There are few subtle points to take into consideration when working with error codes:

*   There is couple of non-POSIX error codes defined by nanomsg library itself (ETERM, EFSM).
*   Some POSIX error codes are not available on all platforms (Windows) and thus are defined by nanomsg library.
*   The numeric values of individual errors differ on various platforms. To make a binding portable, never use numeric values instead of symbolic names of the errors.

Handling EINTR
--------------

EINTR error is used to return the control to the language runtime when Ctrl+C is pressed during a blocking call to nanomsg library, such as nn\_recv().

The right way to handle EINTR is dependent on the specifics of signal handling as implemented by the language runtime. However, if the binding is implemented in the native language (rather than as a module written in C) simply re-starting the interrupted function should be (in most cases) the right way to handle the error.

Polling
-------

Polling mechanism, given that it is a glue between disparate types of subsystems (file systems, networking stack, etc.) must be defined by the platform rather than by any individual subsystem (such as nanomsg). Thus, binding developer should try to integrate nanomsg into the native polling mechanism. File descriptors retrieved from the socket using NN\_SNDFD and NN\_RCVFD socket options can be used for this purpose.

If the language doesn't provide a native polling mechanism or if it doesn't provide a way to plug arbitrary file descriptors into the native polling mechanism, then the binding should do the second best thing and implement a polling function/object itself.

Modularity
----------

nanomsg implements multiple scalability protocols. To be super-consistent it should have been split into multiple separate libraries, however, that would be a management burden. So, instead of multiple libraries, nanomsg, provides the common API (basically just generic BSD sockets) in nn.h header and defines a specific header file for each protocol. These headers define any constants or functions specific to the individual protocols. For example "NN\_PUB" socket type and "NN\_SUB\_SUBSCRIBE" socket option are specifc to pub/sub protocol and thus they are defined in <nanomsg/pubsub.h> header file.

This separation prevents nanomsg developers to unintentionally drag in any inter-protocol dependencies and keeps every scalability protocol usable even in absence of its siblings.

Language binding authors should consider whether this kind of modularity is worth implementing in the binding.

The rule of the thumb is: If the binging is simple enough and does little more than forwarding the calls from the user to the nanomsg library, the separation is not necessary. However, if the binding provides non-trivial functionality of its own, keeping the protocols separate makes sense to prevent accidental dependencies between the protocols.

**March 28th, 2013**
