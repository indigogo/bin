#!/usr/bin/python

import os
import sys

if( len( sys.argv ) < 2 ):
	print "args:\tpdbfile\t<incl_hetatms(T|F)>"
	sys.exit()
sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
try:
	incl_hetatms = sys.argv.pop( 0 ).lower()
	if incl_hetatms == 't':
		incl_hetatms = True
	else:
		incl_hetatms = False
except:
 	incl_hetatms = False


pdbfile = open( pdbname, 'r' )
pdb = pdbfile.readlines()
chain_ids = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefgghijklmnopqrstuvwxyz')

name = '.'.join( pdbname.split('.')[ :-1 ] )
pdbout = open( name + '.addchain.pdb', 'w' )

chain = chain_ids.pop( 0 )
first_line = True
pdb_chains = []
for i in range( len( pdb ) ):
	#skip hetatms, hydrogens, non-prot
	line = pdb[ i ]
	line = line.rstrip()
	if incl_hetatms == True:
		if not ( line[ 0:4 ].startswith( 'ATOM' ) or line[ 0:6 ].startswith( 'HETATM' ) ): continue
	else:
		if not ( line[ 0:4 ].startswith( 'ATOM' ) ): continue

	#if new residue, run search for previous res, then clear sc line cache
	this_resnum = int( line[ 22:26 ].strip() )
	this_chain = line[ 21 ]
	if this_chain not in pdb_chains:
		pdb_chains.append( this_chain )
	if not first_line:
		if this_chain != last_chain:
			try:
				chain = chain_ids.pop( 0 )
			except:
				print( 'ERROR: Too many chains, we ran out of valid characters to assign as chain IDs!!\n' )
				sys.exit()
	else: first_line = False
	last_resnum = this_resnum
	last_chain = this_chain
	pdbout.write( line[ :21 ] + chain + line[ 22: ] + '\n' )

