#!/bin/zsh

dir1=$1
dir2=$2

# Define the patterns for files and directories to be ignored
ignore_patterns=("*.DS_Store" "*/.localized" "*/Thumbs.db" "*/desktop.ini" "*/.TemporaryItems" "*/.Spotlight-V100" "*/.Trashes" "*/.Trash-*")

# Generate the --exclude parameters for the diff command
exclude_params=()
for pattern in "${ignore_patterns[@]}"; do
  exclude_params+=("--exclude=$pattern")
done

# Run diff command, excluding files and directories matching the ignore patterns
diff_output=$(diff -rq "${exclude_params[@]}" "$dir1" "$dir2" | grep -E '^Only in '"$dir1" | cut -d: -f2-)

if [[ -z $diff_output ]]; then
  echo "No left-to-right differences found."
else
  echo "Left-to-right differences:"
  echo "$diff_output"
fi

