
for i in range(1, 161):
  with open('%d/blog.md' % i, 'r') as f:
    c = f.read()
  lines = c.strip().split('\n')
  title = lines[0][2:]
  date = lines[-1][2:-2]
  meta = """{"title": "%s", "date": "%s"}""" % (title, date)
  with open("%d/meta.json" % i, "w") as f:
    f.write(meta)

