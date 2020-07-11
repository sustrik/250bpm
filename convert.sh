#!/usr/bin/env bash

showdown makehtml -i all.md -o all.html

for d in *; do
  if [ -d "$d" ]; then
    echo "$d"
    showdown makehtml -i $d/blog.md -o $d/r.html
    cat header.html $d/r.html footer.html > $d/t.html
    rm $d/r.html
    ln -s $d/t.html blog:$d
  fi
done
