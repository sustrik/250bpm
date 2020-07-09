# Idiot's Guide to ABI Versioning



Libtool ABI versioning is used in both nanomsg and ZeroMQ, so I've been dealing with it for a long time now.

However, for some not completely obvious reason it seems almost impossible to remember how it works. I've observed myself as well as other people forgetting the rules over and over again.

This short article is my attempt to formulate libtool ABI versioning rules in such a way that they can be actually remembered.

First of all, don't think of the ABI version major/minor/patch version, e.g. "4.23.1", rather, think of it as just major/minor version ("4.23") with a special additional number called "age" which is conceptually different from the other two numbers. The right way to think of that particular ABI version is thus "version 4.23, age 1".

Major and minor (called _current_ and _revision_ in libtool terminology) work exactly as you would expect them to work. The only rule to follow is that any change to ABI requires new major version. Thus, minor versions are used only to distinguish between versions that have exactly the same interface but different implementations.

"Age" is the confusing part. What it refers to is backward compatibility. Specifically, how many major versions are backward compatible with the current one. In case of "version 4.23, age 1" there's exactly one old major version (3.x) compatible with the current major version (4.x), thus, if you have code compiled with version 3.x it should still work if you link it to 4.x library.

And that's it.

For canonical info on libtool versioning look here:

[http://www.gnu.org/software/libtool/manual/html\_node/Libtool-versioning.html](http://www.gnu.org/software/libtool/manual/html_node/Libtool-versioning.html)  
[http://www.gnu.org/software/libtool/manual/html\_node/Updating-version-info.html](http://www.gnu.org/software/libtool/manual/html_node/Updating-version-info.html)

**Martin Sústrik, Jun 10th, 2014**