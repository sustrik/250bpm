#!/usr/bin/env bash

md-to-html --input all.md --output all.html

for d in *; do
  if [ -d "$d" ]; then
    echo "$d"
    md-to-html --input $d/blog.md --output $d/t.html
  fi
done
