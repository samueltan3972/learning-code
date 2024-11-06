#!/bin/bash

input_dir=./folder

# Method 1 - find
find "$input_dir" -type f -iname "*.pdf" | while read -r file; do
    # Get the filename without the path
    filename=$(basename "$file")
    
    echo $filename
done

# Method 2 - Process substitution
while read -r file; do
    # Get the filename without the path
    filename=$(basename "$file")
    
    echo $filename
done < <(find "$input_dir" -type f -iregex '.*\.\(jpg\|jpeg\|png\)$')