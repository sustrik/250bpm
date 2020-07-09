import os
from urllib.request import urlopen

for i in range(17, 161):
  print(i)
  html = urlopen("http://250bpm.com/blog:%d" % i).read().decode('utf-8')
  os.mkdir(str(i))
  with open("%d/blog.html" % i, "w") as f:
    f.write(html)

