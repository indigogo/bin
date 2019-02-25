#!/usr/bin/python

import os
import sys
import string

if( len( sys.argv ) < 2 ):
	print "args:\tpdbfile"
	sys.exit()
sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )

pdbfile = open( pdbname, 'r' )
pdb = pdbfile.readlines()
chains = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

name = '.'.join( pdbname.split('.')[ :-1 ] )
pdbout = open( name + '.seqres.pdb', 'w' )


chain = chains.pop( 0 )
first_line = True
resnum = 1
for i in range( len( pdb ) ):
	#skip hetatms, hydrogens, non-prot
	line = pdb[ i ]
	line = line.rstrip()
#	if not ( line[ 0:4 ].startswith( 'ATOM' ) or line[ 0:6 ].startswith( 'HETATM' ) ): continue
	if not line[ 0:4 ].startswith( 'ATOM' ): continue

	#if new residue, run search for previous res, then clear sc line cache
	this_resnum = int( line[ 22:26 ].strip() )
	this_chain = line[ 21 ]
	if not first_line:
		if this_resnum < last_resnum or this_chain != last_chain:
			resnum += 1
			chain = chains.pop( 0 )
		elif this_resnum != last_resnum or this_chain != last_chain:
			resnum += 1
	else: first_line = False
	last_resnum = this_resnum
	last_chain = this_chain
	resnum_str = '%4.0f' % resnum
	pdbout.write( line[ :21 ] + chain + resnum_str + line[ 26: ] + '\n' )

