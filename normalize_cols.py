#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tfile\tcols"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
cols = sys.argv

file = open( filename, 'r' ).readlines()
min = [ 0 ] * len( file[ 0 ].split() )
max = [ 0 ] * len( file[ 0 ].split() )
#preload min/max w/ first vals
vals = file[ 0 ].split()
for col in cols:
	ival = int( col ) - 1
	min[ ival ] = float( vals[ ival ] )
	max[ ival ] = float( vals[ ival ] )
#now get min/max
for line in file:
	vals = line.split()
	for col in cols:
		ival = int( col ) - 1
		val = float( vals[ ival ] )
		if float( val ) < min[ ival ]: min[ ival ] = float( val )
		if float( val ) > max[ ival ]: max[ ival ] = float( val )
#transform vals
for line in file:
	vals = line.split()
	for ival in range( len( vals ) ):
		val = vals[ ival ]
		if str( ival + 1 ) in cols:
			val = float( val )
			val = ( val - min[ ival ] ) / ( max[ ival ] - min[ ival ] )
		print str( val ) + '\t',
	print
