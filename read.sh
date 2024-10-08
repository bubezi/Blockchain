#!/bin/bash

# Define the root directory where your files are located
ROOT_DIR="./"

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

