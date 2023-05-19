#!/bin/bash

directory="downloads/"

# Create the directory
mkdir -p "$directory"

# Check if the directory was created successfully
if [ $? -eq 0 ]; then
    echo "Directory '$directory' created successfully."
else
    echo "Failed to create directory '$directory'."
fi

