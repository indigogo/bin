#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	cols = sys.argv
except:
	print "args:\tfile\tcol_header_tags"
	sys.exit()

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

header_list = file.pop( 0 ).rstrip().split()
header = dict( zip( header_list, range( len( header_list ) )  ) )
ncols = []
for col in cols:
	ncols.append( header[ col ] )

for line in file:
	toks = line.rstrip().split()
	for ncol in ncols:
		sys.stdout.write( toks[ ncol ] + '\t' )
	sys.stdout.write( '\n' )

