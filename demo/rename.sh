#!/bin/bash

# Define the initial offset
offset=0
index=0
fix=1000000

mkdir -p collection
# Loop through each directory in the current directory
for dir in */; do
  # Skip the "collection" directory if it exists
  if [ "$dir" == "collection/" ]; then
    continue
  fi
  # Loop through each file in the directory that matches the pattern "image*.png"
  for file in "${dir}"image*.png; do
    # Extract the number from the file name
    number=$(echo "$file" | sed 's/.*image\([0-9]*\)\.png/\1/')
    # Add the offset to the number
    #new_number=$(expr $number + $offset + $fix)
    new_number=$(expr $index + $fix)
    # Rename the file with the new number
    mv "$file" "${dir}image${new_number}.png"
    index=$(expr $index + 1)
  done
  
  for file in "${dir}"image*.png; do
    # Extract the number from the file name
    number=$(echo "$file" | sed 's/.*image\([0-9]*\)\.png/\1/')
    # Add the offset to the number
    new_number=$(expr $number - $fix)
    # Rename the file with the new number
    mv "$file" "${dir}image${new_number}.png"
    # Copy the file to the "collection" directory
    cp "${dir}image${new_number}.png" "collection/"
  done

  # Update the offset for the next directory
  last_file=$(ls "${dir}"image*.png | tail -n 1)
  last_number=$(echo "$last_file" | sed 's/.*image\([0-9]*\)\.png/\1/')
  offset=$(expr $last_number + 1)
done
