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

out = ''
for blog in sorted(titles.items()):
  out += "* [%s](/blog:%d)\n" % (blog[1], blog[0])

with open("toc.md", "w") as f:
    f.write(out)

