#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
tag = sys.argv.pop( 0 )
scale = float( sys.argv.pop( 0 ) )

file = open( filename, 'r' )
for line in file:
	if tag in line:
		parse = line.split( ',' )	
		for i in range( 9, len( parse ) ):
			if not parse[ i ]:
				n_commas = len( parse ) - i
				break
			newval = scale * float( parse[ i ] )
			parse[ i ] = str( newval )
		line = ','.join( parse )
	print line,
