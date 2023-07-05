#!/bin/zsh

dir1=$1
dir2=$2

diff_output=$(diff -rq "$dir1" "$dir2" | grep -E '^Only in '"$dir1" | cut -d: -f2-)

if [[ -z $diff_output ]]; then
  echo "No left-to-right differences found."
else
  echo "Left-to-right differences:"
  echo "$diff_output"
fi

