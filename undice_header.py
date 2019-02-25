#!/usr/bin/python

import sys
import os
import math

filenames = sys.stdin.readlines()
if( len( sys.argv ) < 2 or len( filenames ) < 2 ):
	print "args:\tSTDIN(filenames)\toutname"
	sys.exit()
sys.argv.pop( 0 )
outname = sys.argv.pop( 0 )

combined = []
for ifilename in range( len( filenames ) ):
	filename = filenames[ ifilename ]
	filename = filename.rstrip()
	file = open( filename, 'r' ).readlines()
	if ifilename != 0: file.pop( 0 )
	for line in file: combined.append( line )
out = open( outname, 'w' )
out.writelines( combined )
out.close()
