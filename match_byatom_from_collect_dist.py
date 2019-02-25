#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tcollect_distribution_stdout\tmatch_to"
	sys.exit()
sys.argv.pop( 0 )
file1name = sys.argv.pop( 0 )
file2name = sys.argv.pop( 0 )

file1 = open( file1name, 'r' ).readlines()
file2 = open( file2name, 'r' ).readlines()
for line in file1:
	line = line.rstrip()
	parse = line.split()
	if parse[ 0 ] != 'pilot.chrisk.collect_distribution:' or parse[ 1 ] == 'collecting':
		continue
	#get ref vals
	pdbname = parse[ 1 ]
	dist = parse[ 2 ]
	rsd1 = parse[ 5 ]
	seqpos1 = parse[ 6 ]
	atom1 = parse[ 7 ]
	rsd2 = parse[ 10 ]
	seqpos2 = parse[ 11 ]
	atom2 = parse[ 12 ]
	val = parse[ 13 ]
	#parse out pdb tag
	pdbname = pdbname.split( '/' )[ -1 ][ :4 ]
	#now match and print val2 over file2
	for matchline in file2:
		matchline = matchline.rstrip()
		matchparse = matchline.split()
		if matchparse[ 0 ] != 'pilot.chrisk.collect_distribution:' or matchparse[ 1 ] == 'collecting':
			continue
		matchpdbname= matchparse[ 1 ]
		matchpdbname = matchpdbname.split( '/' )[ -1 ][ :4 ]
		if matchpdbname != pdbname: continue
		if matchparse[ 2 ] != dist: continue
		if matchparse[ 5 ] != rsd1: continue
		if matchparse[ 6 ] != seqpos1: continue
		if matchparse[ 7 ] != atom1: continue
		if matchparse[ 10 ] != rsd2: continue
		if matchparse[ 11 ] != seqpos2: continue
		if matchparse[ 12 ] != atom2: continue
		matchval = matchparse[ 13 ]
		print ' '.join( [ pdbname, dist, rsd1, seqpos1, atom1, rsd2, seqpos2, atom2, val, matchval ] )
		continue
