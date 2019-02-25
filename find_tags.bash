#!/bin/bash
find kinase/pka -maxdepth 1 -type d -name '*1l3r_test*08*' | awk -F '/' '{print $3}' | awk -F '_1l3r_test_' '{print $1" "$NF}'
#find kinase/pka -maxdepth 1 -type d -name '*1l3r_native*0[87]*' | awk -F '/' '{print $3}' | awk -F '_1l3r_native_' '{print $1" "$NF}'
#find pdz/erbin/ -maxdepth 1 -type d -name '*1mfg_test*08*' | awk -F '/' '{print $4}' | awk -F '_1mfg_test_' '{print $1" "$NF}'

