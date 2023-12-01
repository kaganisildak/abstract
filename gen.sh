#!/bin/bash

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <output name> [debug]"
    exit 1
fi

# The first argument
out_name=$1

# Base command
command="manim scenes/bb3.py BB3 -o $out_name"

# Check if the second argument is 'debug'
if [ "$2" == "debug" ]; then
    command+=" -pql"
fi

# Execute the command
echo "Executing: $command"
eval $command
