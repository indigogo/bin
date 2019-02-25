#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )

file = open( filename, 'r' )

aas = [ 'ALA', 'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN', 'PRO', 'GLN', 'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR' ]
for aa in aas:
	if os.path.exists( aa + '.' + filename ): os.remove( filename )

for line in file:
	for aa in aas:
		if line.find( aa ) != -1:
			resfilename = aa + '.' + filename
			resfile = open( resfilename, 'a' )
			resfile.write( line )

