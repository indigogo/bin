#!/usr/bin/python

import sys
import os

aa3_to_aa1 = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
              'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
              'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
              'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
							'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

if( len( sys.argv ) < 2 ):
	print "args:\tfasta\tchainID\tpdbfile\t<fasta_start_res>"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
chain = sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
if( len( sys.argv ) > 0 ): ires1 = int( sys.argv.pop( 0 ) )
else: ires1 = 1

file = open( filename, 'r' ).readlines()
seq = ''
for line in file:
	if line[ 0 ] == '>': continue
	seq += line.strip()

ires1_pdb = None
pdb_res = {}
pdb = open( pdbname, 'r' ).readlines()
for il,line in enumerate( pdb ):
  if not line.startswith( 'ATOM' ): continue
  if chain is None: chain = line[ 21 ]
  elif line[ 21 ] != chain: continue
  #store res index of existing residue (in case of missing res)
  ires_pdb = int( line[ 22:26 ].strip() )
  aa1_pdb = aa3_to_aa1[ line[ 17:20 ] ]
  if ires_pdb not in pdb_res: pdb_res[ ires_pdb ] = aa1_pdb
  if ires1_pdb is None:
    ires1_pdb = ires_pdb

print 'NATAA\nstart'
for i in range( len( seq ) ):
	ires_pdb = i + ires1_pdb
	#skip this res if it's not in the pdb
	if ires_pdb not in pdb_res.keys(): continue
	if pdb_res[ ires_pdb ] == seq[ i ]: continue
	if seq[ i ] == 'X': print str( ires_pdb ), chain, 'ALLAAxc'
	else: print str( ires_pdb ), chain, 'PIKAA', seq[ i ]
