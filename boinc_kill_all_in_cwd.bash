#!/bin/bash
grep 'name' *.boinc | perl -lane '$_=~s/.*name\s*=\s*//; chomp( $_ ); `/work/boinc/bin/boinc_resize_by_name $F[0] -size 1 >> qq `' &
