#!/usr/bin/env python3

import html
import os
import datetime
import re

class Blog:
  def __init__(self, content):
    self.title = content.strip().split('\n')[0][2:]
    date = re.search(r"^\*\*(\w{3})\w* (\d+)\w+, (\d+)\*\*$", content, re.M)
    if not date:
      raise Exception("No date found in: %s" % self.title)
    self.date = datetime.datetime.strptime(' '.join(date.groups()), '%b %d %Y')

# collect blogs
blogs = {}
for d in os.listdir():
  if not os.path.isdir(d):
    continue
  if not d.startswith('blog:'):
    continue
  num = int(d[5:])
  with open(d + '/blog.md', 'r') as f:
    c = f.read()
  blogs[num] = Blog(c)

blogs = sorted(blogs.items())
blogs.reverse()

def fmt(blog, root='.'):
  return "* [%s](%s/blog:%d/index.html)\n" % (blog[1].title, root, blog[0])

out = """
<img class="logo" src="250bpm.png">

<h1><b>THIS BLOG WAS MOVED TO <a href="https://250bpm.substack.com">SUBSTACK</a>.</b></h1>

My name is Martin Sústrik. In the past I have written software projects such as [ØMQ](https://zeromq.org/), [nanomsg](https://nanomsg.org) or [libdill](https://libdill.org). I may have been the first one to use the term [structured concurrency](https://en.wikipedia.org/wiki/Structured_concurrency). These days I blog about random stuff.

All the opinions stated here are my own. Any resemblance to opinions of other people, living or dead, is purely coincidental.

<img src="rss.png" class="rss"> [RSS feed](rss.xml)

"""

out += '### Recent\n\n'
for i in range(0, 5):
  out += fmt(blogs[i])

out += '### Sociology, Evolution, Coordination Problems\n\n'
for i in [177, 176, 175, 174, 172, 165, 163, 162, 161, 160, 159, 151, 136, 135, 132, 128, 127, 125, 113, 100, 96, 94, 92, 66]:
  out += fmt(blogs[-i]) 

out += '### Structured Concurrency\n\n'
for i in [146, 145, 143, 139, 137, 124, 71, 70, 69, 25]:
  out += fmt(blogs[-i])

out += '### Miscellanea\n\n'
for i in [153, 152, 149, 133, 121, 119, 102, 95, 93, 91, 88, 81, 68, 65, 55, 51, 50, 49, 48, 45]:
  out += fmt(blogs[-i])

out += """### Software
* [ØMQ](https://zeromq.org/) - a distributed messaging library
* [nanomsg](https://nanomsg.org) - a distributed messaging library
* [libdill](https://libdill.org) - [structured concurrency](http://libdill.org/structured-concurrency.html), in C
* [cartesian](https://github.com/sustrik/cartesian) - playing around with the idea of [cartesian programming paradigm](file:///home/martin/250bpm/blog:91/index.html)
* [tiles](https://github.com/sustrik/tiles) - code generator manipulating [rectangular areas of text](file:///home/martin/250bpm/blog:147/index.html)
* [grison](https://github.com/sustrik/grison) - storing structures with cycles in JSON

"""

out += '### Short Stories\n\n'
for i in [164, 150, 134, 131, 130, 129, 109]:
  out += fmt(blogs[-i])  

out += '### Moments Musicaux\n\n'
for i in [148, 84, 79]:
  out += fmt(blogs[-i])

out += '### All articles\n\n'
out += '* [All articles](toc/index.html)\n\n'

with open("index.md", "w") as f:
  f.write(out)

out = '# All artices\n'
for blog in blogs:
  out += fmt(blog, root='..')
with open("toc/blog.md", "w") as f:
  f.write(out)

rss = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>250bpm</title>
  <link>http://250bpm.com</link>
  <description>Martin Sustrik's Blog</description>
"""
for blog in blogs:
  desc = html.escape(blog[1].title)
  link = "http://250bpm.com/blog:%s" % blog[0]
  date = blog[1].date.strftime('%a, %d %b %Y %H:%M:%S GMT')
  rss += """
  <item>
    <title>%s</title>
    <link>%s</link>
    <description>%s</description>
    <pubDate>%s</pubDate>
  </item>""" % (desc, link, desc, date)
rss += """
</channel>
</rss>
"""
with open("rss.xml", "w") as f:
  f.write(rss)
