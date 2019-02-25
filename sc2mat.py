#!/usr/bin/python

#################################################################

import os
import sys
import math

if( len( sys.argv ) < 2 ):
	print "args:\tscfile"
	sys.exit()
sys.argv.pop( 0 )
scname = sys.argv.pop( 0 )

scfile = open( scname, 'r' )
sc = scfile.readlines()
matname = scname[ 0:scname.rfind( '.' ) ] + '.scmat'
matfile = open( matname, 'w' )
keyname = scname[ 0:scname.rfind( '.' ) ] + '.sckey'
keyfile = open( keyname, 'w' )
pdbsname = scname[ 0:scname.rfind( '.' ) ] + '.scpdb'
pdbsfile = open( pdbsname, 'w' )

reading = False
for i in range( len( sc ) ):
	line = sc[ i ]
	line = line.rstrip()
	parse = line.split()

	#header when first elem is SCORE
	if not reading and parse[ 0 ] == 'SCORE:':
		parse.pop( 0 )
		parse.pop()
		keyfile.write( '\n'.join( parse ) + '\n' )
		reading = True
		continue
	elif reading:
		parse.pop( 0 )
		pdbsfile.write( parse.pop() + '\n' )
		matfile.write( '\t'.join( parse ) + '\n' )
