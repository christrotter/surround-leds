#!/bin/bash
# cp /Volumes/CIRCUITPY/ $[a-z]*.py .

# the file path is: /Volumes/CIRCUITPY/
# a valid filename is file.py
# an invalid filename is _file.py

for file in /Volumes/CIRCUITPY/*; do
    if [[ $file =~ ^[a-zA-Z0-9_]+\.py$ ]]; then
        echo "Invalid file: $file"
    else
        cp "$file" ./
        echo "Copied file: $file"
    fi
done

