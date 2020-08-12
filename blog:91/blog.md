# Sure, we have imperative and functional. But what about cartesian programming?



Recently, I've released a small tool to write configurations ([repo](https://github.com/sustrik/cartesian)). The README is pragmatic, just a worked example, and doesn't claim anything extraordinary. However, my ultimate motive was to explore a new programming paradigm, or at least a paradigm that I — being a programmer for three dacades — have never heard of.

Describing the world using cartesian products isn't logical programming or object-oriented programming. It isn't functional programming in the strict sense and it's definitely not imperative programming.

I am not making any big claims now either, mind you. I would just like to explore the mechanics and the limits of this new paradigm. Maybe its use is limited to the niche area of writing config files? Or maybe it's a full-blown paradigm, a worthwhile peer to functional and imperative paradigms? I frankly don't know.

That being said, I want to address an obvious objection to the cartesian paradigm. The objection goes like this: "Cartesian program generates a description of the world in the form of a set of anonymous (unnamed) objects. You can iterate over them, but you cannot really reference any specific object. This makes the paradigm not useful for anything but config files, which don't, by their nature, require addressable objects."

To put it in practical terms, what if we wanted one object to be dependent on another object? Say, what if we wanted property X of object A to be twice the property X of object B:

<img class="old" src="matrix2.png">

How would you write getter function for property X? Two times what exactly?

    var cfg = {
        x: alt(0, 1, 2, 3),
        y: alt(0, 1, 2, 3),
        z: alt(0, 1, 2, 3),
        get x() {
            if(this.x == 3 && this.y == 3 && this.z == 3) {
                return 2 * ????
            }
            ...
        }
    }

Well, I think (prove me wrong, if you can) that this problem is really in the eye of the beholder. As long as you think as described above there's no way to solve the problem. However, once you start thinking in top-down manner rather than traditional bottom-up manner, the problem disappears. Let me explain.

In both imperative and funcional paradigms we are accustomed to start with smallest functions and then to combine them into more complex functional units.

Now have a look at a possible solution of our original problem:

    var global = {
        base: 1,
        get expanded() {return this.base * 2}
    }
    
    var cfg = {
        x: alt(0, 1, 2, 3),
        y: alt(0, 1, 2, 3),
        z: alt(0, 1, 2, 3),
        get x() {
            if(this.x == 3 && this.y == 3 && this.z == 3) return global.expanded
            return global.base
        }
    }

What's going on here?

We've solved the problem by creating an object with a bigger scope (a global one) and referencing it from the smaller-scoped object (our configuration). Note that in both imperative and functional programming it works exactly the other way round: Bigger-scoped objects invoke smaller-scoped functions to solve problems in subdomains of their original problem.

Now, the above may look like just a nasty hack to get the desired behaviour. Before passing such verdict though, let's have a look at a worked real-world-like example.

Let's say we want to configure our production deployment in such a way that we run ten backend servers for each web server. We also have multiple datacenters, each running different number of web servers:

    var newyork = {
        name: 'newyork',
        webservers: 7
    }
    
    var london = {
        name: 'london',
        webservers: 4
    }
    
    var tokyo = {
        name: 'tokyo',
        webservers: 2
    }
    
    var plan = {
        datacenter: alt(newyork, london, tokyo),
        get webservers() {return this.datacenter.webservers},
        get backends() {return this.webservers * 10},
    }

Having created the large-scope object (i.e. "global deployment plan") we can use it to create smaller-scoped objects, say, configurations for individual binaries:

    webservers = {
        plan: plan,
        get datacenter() {return this.plan.datacenter.name},
        cmdline: "/usr/bin/webserver",
        get instances() {return this.plan.webservers}
    }
    
    backends = {
        plan: plan,
        get datacenter() {return this.plan.datacenter.name},
        cmdline: "/usr/bin/backend",
        get instances() {return this.plan.backends}
    }

Let's try to expand 'backends' object, delete the 'plan' property that is only an intermediate phase of processing and not interesting in the result and print the whole thing out:

    console.log(JSON.stringify(expand(backends), function(k, v) {
      if(k == 'plan') return undefined
      return v
    }, '  '))

And here's the result, nicely matching our expectations:

    [
      {
        "datacenter": "newyork",
        "cmdline": "/usr/bin/backend",
        "instances": 70
      },
      {
        "datacenter": "london",
        "cmdline": "/usr/bin/backend",
        "instances": 40
      },
      {
        "datacenter": "tokyo",
        "cmdline": "/usr/bin/backend",
        "instances": 20
      }
    ]

So, once again: I am not claiming that cartesian programming is a full-blown paradigm, on a par with logical, functional or imperative programming. However, it seems that the most obvious objection does not really apply.

What are the other objections? I would love to hear about them.

**Apr 30th, 2017**
