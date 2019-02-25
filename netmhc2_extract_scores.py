#!/usr/bin/python

import sys
import os
import re

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
except:
	print "args:\tnetmhc2_output\t<align(f|t)>"
	sys.exit()
try:
	align = sys.argv.pop( 0 )
	if align.lower()[ 0 ] == 't': align = True
	else: align = False
except:
	align = False

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

data = re.compile( '.*\S+\s+\d+\s+[A-Z]+\s+[A-Z]+\s+\d+\.\d+\s+\d+\.\d+\s+' )
for line in file:
	if not data.match( line ): continue
	toks = line.rstrip().split()
	pepseq = toks[ 2 ]
	coreseq = toks[ 3 ]
	score = toks[ 4 ]
	if not align:
		print pepseq, coreseq, score
		continue
	#assuming max 3 extra termini
	pepseq = 'XXX' + pepseq + 'XXX'
	for iseq in range( 3, len( pepseq ) - len( coreseq ) ):
		if pepseq[ iseq:( iseq + len( coreseq ) ) ] == coreseq:
			print pepseq[ ( iseq - 3 ):( iseq + len( coreseq ) + 3 ) ], coreseq, score
			break
	
