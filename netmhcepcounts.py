#!/usr/bin/python

import sys
import os
import re

if( len( sys.argv ) < 2 ):
	print "args:\tnetmhcII_output\tpdbfile\t<cutoff(SB|WB|value)>\t<pdb_chain>"
	sys.exit()
sys.argv.pop( 0 )
mhcname = sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
if len( sys.argv ) > 0: cutoff = sys.argv.pop( 0 )
else: cutoff = 'SB'
if len( sys.argv ) > 0: chain = sys.argv.pop( 0 )
else: chain = None
ep_len = 9

pdb = open( pdbname, 'r' ).readlines()
mhc = open( mhcname, 'r' ).readlines()

# regex to find netmhc data lines w/ binders
epline_str = '.*\d+\s+[A-Z]+\s+\d+\.\d+\s+\d+\s+'
# numerical cutoff or WB/SB match?
try:
	cutoff = float( cutoff )
	num_cut = True
except:
	num_cut = False
	#incl weak binders?
	if cutoff == 'WB':
		epline_str += '[WS]B' 
	elif cutoff == 'SB':
		epline_str += 'SB'
#else matches all lines 
epline = re.compile( epline_str )

#go ahed and get the length of the sequence
ires_nmer_max = 0
for il,line in enumerate( mhc ):
	if not epline.match( line ): continue
	line = line.rstrip().split()
	ires_nmer = int( line[ 0 ] )
	if ires_nmer > ires_nmer_max:
		ires_nmer_max = ires_nmer

#find all mhc 9mers indexed by netmhc output
epi_allele_idxs = []
for il,line in enumerate( mhc ):
	if not epline.match( line ): continue
	line = line.rstrip().split()
	ic50 = float( line[ 3 ] )
	if num_cut and ic50 > cutoff: continue
	ires_nmer = int( line[ 0 ] )
	allele = line[ -1 ]
	nmer = line[ 1 ]
	core = line[ 1 ]
	ires_core = None
	#find first res index of 9mer core inside bigger nmer epitope
	for iseq in range( len( nmer ) - len( core ) + 1 ):
		if nmer[ iseq:( len( core ) + iseq ) ] == core:
			ires_core = ires_nmer + iseq
			break
	if ires_core is None:
		print "ERROR: 9mer ", core, "not found in seq ", nmer, "at line", il
		sys.exit()
	#store tuple of allele name and core index
	epi_allele_idx = ( allele, ires_core, core )
	#only add to list if isn't already there
	if epi_allele_idx not in epi_allele_idxs:
		epi_allele_idxs.append( epi_allele_idx )

#init all to zero
epicounts = {}
for epi_allele_idx in epi_allele_idxs:
	idx = epi_allele_idx[ 1 ]
	core = epi_allele_idx[ 2 ]
	idx_core = ( idx, core )
	if not epicounts.has_key( idx_core ):
		epicounts[ idx_core ] = 1
	else:
		epicounts[ idx_core ] += 1
	
#now match ep res indices to pdb indices, need nterm offset
#this will break only if pdb is missing nterm epitopes
ires1_pdb = None
pdb_res = []
for il,line in enumerate( pdb ):
	if not line.startswith( 'ATOM' ): continue
	if chain is None: chain = line[ 21 ]
	elif line[ 21 ] != chain: continue
	#store res index of existing residue (in case of missing res)
	ires_pdb = int( line[ 22:26 ].strip() )
	if ires_pdb not in pdb_res: pdb_res.append( ires_pdb )
	if ires1_pdb is None:
		ires1_pdb = ires_pdb

#output epitope counts by pdb index
#need to rename blank chain id
if chain == ' ': chain = '_'
for idx_core in sorted( epicounts.iterkeys() ):
	idx = idx_core[ 0 ]
	core = idx_core[ 1 ]
	count = epicounts[ idx_core ]
	idx_ep_pdb = idx + ires1_pdb
	if idx_ep_pdb not in pdb_res: continue
	print str( idx_ep_pdb ), chain, core, str( count )
