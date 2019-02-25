#!/bin/bash
find . -name "$1" -exec md5sum '{}' ';' | sort -k 1 | uniq -w 33 | cut --delimiter=' ' -f 3
