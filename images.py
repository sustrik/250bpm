import wget
from pyquery import PyQuery

for i in range(1, 161):
  with open('%d/blog.html' % i, 'r') as f:
    html=f.read()
  pq = PyQuery(html)
  imgs = pq.find('img')
  for img in imgs:
    src = img.attrib['src']
    if 'avatar' in src or 'pixel.quantserve.com' in src:
      continue
    print(i, src)
    fname = src.split('/')[-1]
    wget.download(src, '%d/%s' % (i, fname))
