#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	chain_str = sys.argv.pop()
except:
	print "args:\tpdb\tchain_str"
	sys.exit()
chain_str = chain_str.upper()
if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

for line in file:
	if not ( line.startswith( 'ATOM' ) or line.startswith( 'HETATM' ) ): continue
	if line[ 21 ] not in chain_str: continue
	sys.stdout.write( line )
