#!/usr/bin/env bash

showdown makehtml all.md -o all.html

for d in *; do
  if [ -d "$d" ]; then
    echo "$d"
    showdown makehtml -i $d/blog.md -o $d/r.html
    cat header.html $d/r.html footer.html > $d/t.html
    rm $d/r.html
  fi
done
