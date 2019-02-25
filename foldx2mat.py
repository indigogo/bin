#!/usr/bin/python

#################################################################

import os
import sys
import math

if( len( sys.argv ) < 2 ):
	print "args:\tfxfile"
	sys.exit()
sys.argv.pop( 0 )
fxname = sys.argv.pop( 0 )

fxfile = open( fxname, 'r' )
fx = fxfile.readlines()
matname = fxname[ 0:fxname.rfind( '.' ) ] + '.fxmat'
matfile = open( matname, 'w' )
keyname = fxname[ 0:fxname.rfind( '.' ) ] + '.fxkey'
keyfile = open( keyname, 'w' )
pdbsname = fxname[ 0:fxname.rfind( '.' ) ] + '.fxpdb'
pdbsfile = open( pdbsname, 'w' )

reading = False
for i in range( len( fx ) ):
	line = fx[ i ]
	line = line.rstrip()
	parse = line.split( '\t' )

	#header when first elem is blank
	if not reading and parse[ 0 ] == '' and len( parse ) > 1:
		parse.pop( 0 )
		keyfile.write( '\n'.join( parse ) + '\n' )
		reading = True
		continue
	elif reading:
		pdbsfile.write( parse.pop( 0 ) + '\n' )
		matfile.write( '\t'.join( parse ) + '\n' )
