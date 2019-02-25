#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
except:
	print "args:\tfilename('-' for stdin)\tcol(idx from 1)"
	sys.exit()
try:
	col = int( sys.argv.pop( 0 ) )
except:
	col = 1

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

sum = 0
for line in file:
	toks = line.rstrip().split()
	sum += float( toks[ col - 1 ] )
print str( sum )
