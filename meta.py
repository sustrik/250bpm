
for i in range(1, 161):
  with open('%d/blog.md' % i, 'r') as f:
    c = f.read()
  lines = c.strip().split('\n')
  print("---- " + str(i))
  print(lines[0])
  print(lines[-1])  


  #with open("all.md", "w") as f:
  #  f.write(out)

