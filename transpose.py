#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tpssm"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )

file = open( filename, 'r' ).readlines()
mat = []
for line in file:
	toks = line.rstrip().split()
	if len( toks ) < 1: continue
	if toks[ 0 ][ 0 ] == '#':
		print line
		continue
	mat.append( toks )
for iel in range( len( mat[ 0 ] ) ):
	for iline in range( len( mat ) ):
		print mat[ iline ][ iel ],
	print
