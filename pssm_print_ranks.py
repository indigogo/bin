#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
except:
	print "args:pssm_file\t"
	sys.exit()

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

#warning: ignores lines 1,2. header key line 3
title = file.pop( 0 )
file.pop( 0 )
aas = file.pop( 0 ).split()
for line in file:
	toks = line.rstrip().split()
	seqpos = toks.pop( 0 )
	nataa = toks.pop( 0 )
	aavals = zip( aas, toks )
	print seqpos, nataa, ': ',
	for aaval in sorted( aavals, key=lambda aaval: float( aaval[ 1 ] ), reverse=True ):
		sys.stdout.write( aaval[ 0 ] + '(' + '%.2f' % float( aaval[ 1 ] ) + ') ' )
	print
	
