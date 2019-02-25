#!/usr/local/bin/python

import sys
import os
from scipy.stats.stats import spearmanr

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	datacol = int( sys.argv.pop( 0 ) ) - 1
	data2col = int( sys.argv.pop( 0 ) ) - 1 
except:
	print "args:\tfile\tdatacol\tdata2col"
	sys.exit()

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

#read data, data2 vals
datavals = []
data2vals = []
for line in file:
	toks = line.rstrip().split()	
	if toks[ 0 ][ 0 ] == '#': continue
	datavals.append( float ( toks[ datacol ] ) )
	data2vals.append( float ( toks[ data2col ] ) )

print filename, spearmanr( datavals, data2vals )[ 0 ]
