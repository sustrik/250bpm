#!/usr/bin/env bash

showdown makehtml -i toc.md -o toc.html
cat header.html toc.html footer.html > index.html

for d in *; do
  if [ -d "$d" ]; then
    echo "$d"
    showdown makehtml -i $d/blog.md -o $d/r.html
    cat header.html $d/r.html footer.html > $d/index.html
    rm $d/r.html
  fi
done
