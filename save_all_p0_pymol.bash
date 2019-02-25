ls *.pdb | grep -v align | awk -F '.pdb' '{print "save "$1".p0.pdb, "$1" and p0 "}'
