#!/bin/sh

#takes in a file containing the constraints for each pdb in the following form: <4-let PDB ID>  constraint1, constraint2,... and outputs
# separate constraints files for each entry
#example for input:
# 1f0n  227A 231A
# 1lwb  112A 120A
# 1ys1  142X 161X

cons=$1

fnames=`awk '{print $1}' $cons`

for f in $fnames; do
  grep $f $cons | awk '{
    for( i=2; i<=NF; i++ ) {
	   print substr($i,1,length($i)-1),substr($i,length($i),1);
	 } }' > $f.constraints
done
