#!/bin/bash

rm list_of_files.txt
for file in templates/*
do
    echo "$file" >> list_of_files.txt
done

export CALIBRE_PYTHON_PATH=/home/carles/git/calibre/src/
calibre-debug -s
calibre-customize -b .
# calibre

# This will save the virtual-shelf in /home/carles/virtual-shelf/index.html
calibredb catalog /home/carles/virtual-shelf.html
