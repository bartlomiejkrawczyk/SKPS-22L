#!/bin/sh
mkdir ../../../histograms/$FOLDER/
mv cli_?.txt ../../../histograms/$FOLDER/
mv server.txt ../../../histograms/$FOLDER/

# Example:
# FOLDER=3_3_3 sh move_files.sh
