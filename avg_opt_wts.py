#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\topt_outfile_list"
	sys.exit()
sys.argv.pop( 0 )
listname = sys.argv.pop( 0 )

list = open( listname, 'r' ).readlines()
scores = {}
n_files = len( list )
first = True
for fname in list:
	fname = fname.rstrip()
	file = open( fname, 'r' ).readlines()
	for line in file:
		line = line.rstrip()
		parse = line.split()
		score = float( parse.pop() )
		tag = ' '.join( parse )
		#if first line, create add entry for dict
		if first: scores[ tag ] = ( score / n_files )
		#else add to sum
		elif tag in scores:
			scores[ tag ] += ( score / n_files )
		#else fail if no matching tag
		else:
			print tag, 'mismatched in file', fname
			sys.exit()	
	#not first at next iteration
	first = False
for tag in sorted( scores, key = scores.get ):
	print tag, scores[ tag ]
