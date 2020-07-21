#!/usr/bin/env bash



./maketoc.py

showdown makehtml -i toc.md -o toc.raw.html
cat header.html toc.raw.html footer.html > toc.html

showdown makehtml -i index.md -o index.raw.html
cat header.html index.raw.html footer.html > index.html

rm toc.md toc.raw.html index.md index.raw.html
exit

for d in *; do
  if [ -d "$d" ]; then
    echo "$d"
    showdown makehtml -i $d/blog.md -o $d/r.html
    cat header.html $d/r.html footer.html > $d/index.html
    rm $d/r.html
  fi
done
