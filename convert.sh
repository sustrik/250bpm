#!/usr/bin/env bash

showdown makehtml all.md -o all.html

for d in *; do
  if [ -d "$d" ]; then
    echo "$d"
    showdown makehtml -i $d/blog.md -o $d/t.html
  fi
done
