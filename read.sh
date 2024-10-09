#!/bin/bash

# Check if a directory argument is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

# Define the root directory where your files are located
ROOT_DIR="$1"

# Check if the provided directory exists
if [ ! -d "$ROOT_DIR" ]; then
  echo "Error: Directory '$ROOT_DIR' does not exist."
  exit 1
fi

# Recursively find all files and loop through them
find "$ROOT_DIR" -type f | while read -r file; do
  # Print the file name
  echo "Displaying content of: $file"
  echo "------------------------------------------------------------"
  # Display the file content
  cat "$file"
  echo
  echo "------------------------------------------------------------"
  echo
done

