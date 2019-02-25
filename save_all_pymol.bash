ls *.pdb | grep -v 'align' | awk -F '\.' '{print "save "$1".align.pdb, "$1}'
