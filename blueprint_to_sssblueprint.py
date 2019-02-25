#!/usr/bin/python

import sys
import os
import re

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
except:
	print "args:\t"
	sys.exit()

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

for iline in range( len( file ) - 1 ):
	line = file[ iline ]
	if not re.match( '^\d+\s+[A-Z]\s+[A-Z]{2}\s+\w$', line ):
		sys.stdout.write( line )
	else:
		# this line is helix or strand and next or prev is loop, change to 'D' any ss
		if re.match( '^\d+\s+[A-Z]\s+[HE][A-Z]\s+\w$', line ) and \
				( re.match( '^\d+\s+[A-Z]\s+[L][A-Z]\s+\w$', file[ iline-1] ) or \
				re.match( '^\d+\s+[A-Z]\s+[L][A-Z]\s+\w$', file[ iline+1] ) ):
			line =	re.sub( r'(^\d+\s+[A-Z]\s+)[HE]([A-Z]\s+\w$)', r'\1D\2', line )
		sys.stdout.write( line )
#print last line
sys.stdout.write( file[ len( file ) - 1 ] )
