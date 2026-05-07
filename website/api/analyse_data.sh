#!/bin/bash

DATE="$1"
DATABASE="$2"
#G5="$3"

#test -n "$G5"
#echo $?

cd /home/wbruce/study_p/core/ && uv run src/analyse/check_data.py -c "$1" -d "$2"  -g5
