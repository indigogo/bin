#!/usr/bin/python

# WARNING: ignores insertion codes and renumbers as sequential res indices!

import os
import sys
import string

if( len( sys.argv ) < 2 ):
	print "args:\tpdbfile\t<reorder_chain(T|F)>\t<reorder_res_by_chain(T|F)>\t<resnum_1(1)>\t<chain_1_char_index(0==A)>"
	sys.exit()
sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
try:
  reorder_chains = sys.argv.pop( 0 )
  if reorder_chains.lower()[ 0 ] == 'f':
		reorder_chains = False
  else: reorder_chains = True
except:
  reorder_chains = True

try:
  reorder_by_chain = sys.argv.pop( 0 )
  if reorder_by_chain.lower()[ 0 ] == 'f':
		reorder_by_chain = False
  else: reorder_by_chain = True
except:
  reorder_by_chain = True

try:
  resnum_1 = int( sys.argv.pop( 0 ) )
except:
  resnum_1 = int( 1 )
try:
  chain_1 = int( sys.argv.pop( 0 ) )
except:
  chain_1 = int( 0 )

print "WARNING: fails with insertion (e.g. res 36A,36B,36C,37)! ignores insertion codes and renumbers as sequential res indices!"

pdbfile = open( pdbname, 'r' )
pdb = pdbfile.readlines()
all_chains = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
chains = all_chains[ chain_1: ]

name = '.'.join( pdbname.split('.')[ :-1 ] )
pdbout = open( name + '.seqres.pdb', 'w' )


if reorder_chains:
	chain = chains.pop( 0 )
first_line = True
resnum = resnum_1
for i in range( len( pdb ) ):
	#skip hetatms, hydrogens, non-prot
	line = pdb[ i ]
	line = line.rstrip()
	if not ( line[ 0:4 ].startswith( 'ATOM' ) or line[ 0:6 ].startswith( 'HETATM' ) ): continue
#	if not line[ 0:4 ].startswith( 'ATOM' ): continue

	#if new residue, run search for previous res, then clear sc line cache
#	this_resnum = int( line[ 22:26 ].strip() ) this line would ignore insertion code differences
	this_resnum = line[ 22:27 ].strip()
	this_chain = line[ 21 ]
	if not first_line:
		if this_resnum != last_resnum or this_chain != last_chain:
			if this_chain != last_chain and reorder_by_chain:
				resnum = resnum_1
			else:
				resnum += 1
			if reorder_chains:
				chain = chains.pop( 0 )
			else:
				chain = this_chain
	else:
		first_line = False
		if not reorder_chains:
			chain = this_chain
	last_resnum = this_resnum
	last_chain = this_chain
	resnum_str = '%4.0f' % resnum
	pdbout.write( line[ :21 ] + chain + resnum_str + line[ 26: ] + '\n' )

