# nanomsg: Towards Full-Blown Configuration Management



There have been no administrative functionality in ZeroMQ, nor there is one in nanomsg. Adding such functionality is currently being discussed on nanomsg mailing list and I feel that it may prove confusing for those not directly involved in the discussion. This blog post thus tries to introduce the basic idea and the use cases without digging too deep into the implementation details.

When you are connecting two components via nanomsg, you typically do it something like this:

    nn_connect (s, "tcp://192.168.0.111:5555");

The problem with that is that the IP address is hardcoded into the executable. When you get to the point of deploying the application from the development environment to the production environment, the IP addresses are going to change. Even if hostnames were used instead of IP addresses, they are going to change when the application is deployed to a different environment. Thus, to be able to do the transition without having to re-compile the executable, you can, for example, pass the connection string as a command line argument:

    $ ./mycomponent tcp://192.168.0.111:5555

And the implementation would look like this:

    nn_connect (s, agv [1]);

The above works OK, however, when there is large number of sockets in the application, the command line approach becomes rather annoying. In such cases people often prefer to use configuration files:

    $ cat mycomponent.config
    socketA tcp://192.168.0.111:5555
    socketB tcp://192.168.0.111:5556
    socketC tcp://192.168.0.23:978

And the corresponding implementation in the component would look something like this:

    nn_connect (s, get_config_option ("myconponent.config", "socketA"));

To understand the full extent of the configuration problem you have to take following facts into account:

1.  The socket can be either connected (nn\_connect) or bound (nn\_bind).
2.  There may be multiple connects and binds on a single socket.
3.  There are certain socket options that should be set be administrator rather than by programmer.

When you build all this flexibility into the configuration file syntax, you'll end up with something like this:

    $ cat mycomponent.config
    socketA sndprio 4
            connect tcp://192.168.0.111:5555
            sndprio 8
            tcp_nodelay 1
            connect  tcp://192.168.0.111:5556
    socketB tcp_nodelay 1
            bind tcp://eth0:978

If even the configuration files are not flexible enough for you, you may want to have all the configuration data stored in some kind of database and let the socket query the database to retrieve the connects, the binds and the socket options. The upside of this approach is that you don't have to distribute the configuration files to all nodes in the system. The downside is that you have to install and maintain the database in the first place.

If you decide to keep the configuration information in a database, even more sophisticated functionality becomes possible. Say, you have 1000 identical blade servers in your datacenter, all of them meant to run the same component. With naive implementation of the configuration database you would have to create 1000 identical records. If you added new server to the cluser you would have to add a new record. Given that all those records are the same, wouldn't it be nicer if you had just one record instead? In such case you wouldn't even have to mess with the database when new server is added to the cluster.

If you decide to implement such functionality, you need some kind of wildcard matching, or even more complex query algorithms built into the configuration service.

At this point, I believe, the enterprise-focused readers can already imagine the future GUI tools that would help you configure the messaging topologies by drawing actual graphs etc.

Now, given that 100% of the applications have this configuration management stuff written by hand, it makes sense to implement it once and let everyone use it.

Furthermore, hand-written configuration management is likely to be limited in some ways and don't allow for the full flexibility discussed above. For example, passing connection string is passed as an command-line argument:

    nn_bind (s, agv [1]);

may seem to be the minimal viable solution. However, it holds only to the point where the admin wants to connect the socket instead of binding it. Call to nn\_bind is hard-coded into the executable and the admin has to modify and re-compile the component — if that is at all possible (consider binary packages!)

To summarise the points above: Current discussion on nanomsg mailing list is about adding a functionality to nanomsg that is required by 100% of the applications and which is very easy to get wrong, if written by hand. Thus, I don't believe it classifies as "unnecessary complexity" or "feature creep".

Finally, let me list some finer questions raised in the discussion:

1.  Should the configuration system be pluggable? In other words, should we allow plugins for MySQL, Redis, DNS, etc. to store the configuration data?
2.  What are the pros and cons of different storage solutions? For example, using DNS to store configuration data feels like a nice solution, because DNS is already installed and running everywhere. You don't have to install and maintain it as you would have to do with MySQL server. It has also nice caching behaviour and even allows for globally accessible configuration records — such as delivering address of a service to the remote clients. The downside, on the other hand, is that write access to DNS is often restricted to network administrators which are not necessarily the same people as those deploying the application.
3.  How should a socket identify itself to the configuration database? In other words, what is the key for configuration records. Socket name? IP address? Hostname? Combination of all the above?
4.  What should be in the body of the configuration records? Should socket options be there? If so, which of them? Etc.

EDIT:

I think I haven't made it clear what's the ultimate goal of the whole endeavour. Let me explain it in form of an use case.

Imagine that we are going to create a distributed application that processes meteorological data. To do so we need a pub/sub topology to distribute the raw meteorological data to individual components.

First, the admin creates the topology by adding a record to DNS, say a TXT record called "meteo-data" with the value of "pub connect tcp:_server001:5555; sub connect tcp:_server001:5556;". Then he starts a pub/sub device at server001.

Second, programmers of individual components connect to the topology by its name rather that to particular IP address or hostname:

    s = nn_socket (AF_SP_CONFIG, NN_PUB);
    nn_connect (s, "meteo-data");

And that's it. As can be seen there are no configuration files, no need to distribute anything or install any additional software etc.

**September 10th, 2013**