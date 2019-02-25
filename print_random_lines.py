#!/usr/bin/python

import sys
import os
import random

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	n = int( sys.argv.pop( 0 ) )
except:
	print "args:file\tn_lines"
	sys.exit()

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

assert( n <= len( file ) ), "n_lines must be <= than total lines"

line_idxs = [ x for x in range( len( file ) ) ]
for ip in range( n ):
	il = random.randint( 0, len( line_idxs ) - 1 )
	sys.stdout.write( file[ line_idxs.pop( il ) ] )
