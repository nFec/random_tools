#!/bin/zsh

dir1=$1
dir2=$2

# Define the pattern for files to be ignored
ignore_pattern='.DS_Store|Thumbs.db|.localized|desktop.ini|.TemporaryItems|.Spotlight-V100|.Trashes|.Trash'

# Run diff command, excluding files matching the ignore pattern
diff_output=$(diff -rq --exclude=$ignore_pattern "$dir1" "$dir2" | grep -E '^Only in '"$dir1" | cut -d: -f2-)

if [[ -z $diff_output ]]; then
  echo "No left-to-right differences found."
else
  echo "Left-to-right differences:"
  echo "$diff_output"
fi

