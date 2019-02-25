#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	col = sys.argv.pop( 0 )
except:
	print "args:\tfile\tcol\tparse_header(t|f)"
	sys.exit()
try:
	has_header = sys.argv.pop( 0 ).lower()
	if has_header == 't': has_header = True
	else: has_header = False
except:
	has_header = False

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

if not has_header: ncol = int( col )
else:
	header_list = file.pop( 0 ).rstrip().split()
	header = dict( zip( header_list, range( len( header_list ) )  ) )
	ncol = header[ col ]

for line in file:
	toks = line.rstrip().split()
	sys.stdout.write( toks[ ncol ] + '\n' )

