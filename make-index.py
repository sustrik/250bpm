from pyquery import PyQuery

out = ''
for i in range(1, 161):
  with open('%d/blog.html' % i, 'r') as f:
    html=f.read()
  pq = PyQuery(html)
  title = pq.find('#page-title').text()
  out += '* [%s](%d/t.html)\n' % (title, i)
print(out)
with open("all.md", "w") as f:
    f.write(out)
