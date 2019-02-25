#!/usr/bin/python

import os
import sys

if( len( sys.argv ) < 2 ):
	print "args:\tpdbfile"
	sys.exit()
sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )

pdbfile = open( pdbname, 'r' )
pdb = pdbfile.readlines()

first_line = True
n_chains = 0
chains = ""
for i in range( len( pdb ) ):
	#skip hetatms, hydrogens, non-prot
	line = pdb[ i ]
	line = line.rstrip()
	if not ( line[ 0:4 ].startswith( 'ATOM' ) or line[ 0:6 ].startswith( 'HETATM' ) ): continue

	#if new residue, run search for previous res, then clear sc line cache
	chain = line[ 21 ]
	if not first_line:
		if chain != last_chain:
			n_chains += 1
			chains += chain
	else:
		n_chains += 1
		chains += chain
		first_line = False
	last_chain = chain

print pdbname, str( n_chains ), chains
