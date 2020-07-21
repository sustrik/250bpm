#!/usr/bin/env python3

import os

# collect blog titles
titles = {}
for d in os.listdir():
  if not os.path.isdir(d):
    continue
  if not d.startswith('blog:'):
    continue
  num = int(d[5:])
  with open(d + '/blog.md', 'r') as f:
    c = f.read()
  title = c.strip().split('\n')[0][2:]
  titles[num] = title

blogs = sorted(titles.items())
blogs.reverse()

def fmt(blog):
  return "* [%s](/250bpm/blog:%d)\n" % (blog[1], blog[0])

out = """
![](/250bpm/250bpm.com)

My name is Martin Sústrik.

Once I have written software projects such as [ØMQ](https://zeromq.org/), [nanomsg](https://nanomsg.org) or [libdill](https://libdill.org).

I believe I was the first one to use the term [Structured Concurrency](https://en.wikipedia.org/wiki/Structured_concurrency).

These days I blog about random stuff.

All the opinions stated here are my own. Any resemblance to opinions of other people, living or dead, is purely coincidental.

"""

out += '### Recent\n\n'
for i in range(0, 5):
  out += fmt(blogs[i])

out += '### Sociology, Politology, History, Coordination Problems\n\n'
for i in [160, 159, 151, 136, 135, 132, 128, 127, 125, 113, 100, 96, 94, 92, 66]:
  out += fmt((i, titles[i]))  

out += '### Short Stories\n\n'
for i in [150, 134, 131, 130, 129, 109]:
  out += fmt((i, titles[i]))  

out += '### Moments Musicaux\n\n'
for i in [148, 84, 79]:
  out += fmt((i, titles[i]))

out += '### All articles\n\n'
out += '* [All articles](toc.html)\n\n'

with open("index.md", "w") as f:
    f.write(out)

out = ''
for blog in blogs:
  out += fmt(blog)
with open("toc.md", "w") as f:
    f.write(out)

