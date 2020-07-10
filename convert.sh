#!/usr/bin/env bash

md-to-html --input all.md --output all.html

for d in *; do
  if [ -d "$d" ]; then
    echo "$d"
    md-to-html --input $d/blog.md --output $d/t.html
    sed -i '5i    <link rel="stylesheet" type="text/css" href="../main.css">' $d/t.html
  fi
done
