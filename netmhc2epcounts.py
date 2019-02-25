#!/usr/bin/python

import sys
import os
import re

if( len( sys.argv ) < 2 ):
	print "args:\tnetmhcII_output\tpdbfile\t<cutoff(SB|WB|value)>\t<pdb_chain>\t<ep_count_min>"
	sys.exit()
sys.argv.pop( 0 )
mhcname = sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
if len( sys.argv ) > 0: cutoff = sys.argv.pop( 0 )
else: cutoff = 'SB'
if len( sys.argv ) > 0: chain = sys.argv.pop( 0 )
else: chain = None
if len( sys.argv ) > 0: ep_count_min = int( sys.argv.pop( 0 ) )
else: ep_count_min = 1

try:
	pdb = open( pdbname, 'r' ).readlines()
except:
	pdb = []
mhc = open( mhcname, 'r' ).readlines()

# regex to find netmhc data lines
pepline_str = '.*\S+\s+\d+\s+[A-Z]+\s+[A-Z]+\s+\d+\.\d+\s+\d+\.\d+\s+.*'
# regex to find netmhc data lines w/ binders
epline_str = pepline_str
# numerical cutoff or WB/SB match?
try:
	cutoff = float( cutoff )
	num_cut = True
except:
	num_cut = False
	#incl weak binders?
	if cutoff == 'WB':
		epline_str += '\s+[WS]B\s+' 
	elif cutoff == 'SB':
		epline_str += '\s+SB\s+'
#else matches all lines 
pepline = re.compile( pepline_str )
epline = re.compile( epline_str )

##go ahed and get the length of the sequence
#ires_nmer_max = 0
#for il,line in enumerate( mhc ):
#	if not pepline.match( line ): continue
#	line = line.rstrip().split()
#	ires_nmer = int( line[ 1 ] )
#	if ires_nmer > ires_nmer_max:
#		ires_nmer_max = ires_nmer

#find all mhc 9mers indexed by netmhc output
epi_allele_idxs = []
for il,line_str in enumerate( mhc ):
	if not pepline.match( line_str ): continue
	line = line_str.rstrip().split()
	ic50 = float( line[ 5 ] )
	ires_nmer = int( line[ 1 ] )
	allele = line[ 0 ]
	nmer = line[ 2 ]
	core = line[ 3 ]
	ires_core = None
	#find first res index of 9mer core inside bigger nmer epitope
	for iseq in range( len( nmer ) - len( core ) + 1 ):
		if nmer[ iseq:( len( core ) + iseq ) ] == core:
			ires_core = ires_nmer + iseq
			break
	if ires_core is None:
		print "ERROR: 9mer ", core, "not found in seq ", nmer, "at line", il
		sys.exit()
	#store tuple of allele name, index, 9mer seq, is_ep(bool)
	is_ep = False
	if num_cut and ic50 <= cutoff: is_ep = True
	elif epline.match( line_str ): is_ep = True
	epi_allele_idx = ( allele, ires_core, core, is_ep )
	#only add to list if isn't already there
	if epi_allele_idx not in epi_allele_idxs:
		epi_allele_idxs.append( epi_allele_idx )

#init all to zero
epicounts = {}
for epi_allele_idx in epi_allele_idxs:
	idx = epi_allele_idx[ 1 ]
	core = epi_allele_idx[ 2 ]
	is_ep = epi_allele_idx[ 3 ]
	idx_core = ( idx, core )
	if not epicounts.has_key( idx_core ):
		epicounts[ idx_core ] = int( is_ep )
	else:
		epicounts[ idx_core ] += int( is_ep )
	
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
#if no pdb supplied, set to dummy val 0
if ires1_pdb is None: ires1_pdb = 0

#output epitope counts by pdb index
#need to rename blank chain id
if chain == ' ': chain = '_'
for idx_core in sorted( epicounts.iterkeys() ):
	idx = idx_core[ 0 ]
	core = idx_core[ 1 ]
	count = epicounts[ idx_core ]
	if count < ep_count_min: continue
	idx_ep_pdb = idx + ires1_pdb
	#only check for pdb indices if we provided a real pdb
	if len( pdb ) > 0 and idx_ep_pdb not in pdb_res: continue
	print str( idx_ep_pdb ), chain, core, str( count )
