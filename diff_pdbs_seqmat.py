#!/usr/bin/python

import sys
import os

aa3_to_aa1 = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
              'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
              'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
              'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
              'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

#get dict of chain-->seqpos-->aa3 for a pdb
def get_chain_seqpos_aa3s( pdb, use_chain ):
	chain_seqpos_aa3s = {}
	for line in pdb:
		if not ( len( line ) > 20 ): continue
		if not ( line[0:4] == 'ATOM' or (line[0:6] == 'HETATM') & (line[17:20]=='MSE') ): continue
		chain = line[ 21 ]
		if use_chain != False and chain != use_chain:
			continue
		if chain == ' ': chain = '_'
		seqpos = int( line[23:26].strip() )
		aa3 = line[17:20].strip()
		#init this chain key if not isdef
		if not chain_seqpos_aa3s.has_key( chain ):
			chain_seqpos_aa3s[ chain ] = {}
		#skip if we've already stored this chain,seqpos aa3
		elif chain_seqpos_aa3s[ chain ].has_key( seqpos ): continue
		chain_seqpos_aa3s[ chain ][ seqpos ] = aa3
	return chain_seqpos_aa3s

# mutmapis a dict of dicts of point mutations
def add_mut_data_to_mutmap( mutmap_args ):
	pdb1name = mutmap_args[ 0 ]
	pdb2name = mutmap_args[ 1 ]
	mutmap = mutmap_args[ 2 ]
	chain_in = mutmap_args[ 3 ]
	pdb1 = open( pdb1name, 'r' ).readlines()
	pdb2 = open( pdb2name, 'r' ).readlines()
	pdb1_chain_seqpos_aa3s = get_chain_seqpos_aa3s( pdb1, chain_in )
	pdb2_chain_seqpos_aa3s = get_chain_seqpos_aa3s( pdb2, chain_in )

	
	checked_any_pairs = False
	#save all elements of 2 dicts where aa3 doesn't match
	#skip if chain,seqpos isn't in pdb2
	for chain in sorted( pdb1_chain_seqpos_aa3s.iterkeys() ):
		if not( pdb2_chain_seqpos_aa3s.has_key( chain ) ): continue
		for seqpos in sorted( pdb1_chain_seqpos_aa3s[ chain ].iterkeys() ):
			if not( pdb2_chain_seqpos_aa3s[ chain ].has_key( seqpos ) ): continue
			checked_any_pairs = True
			# ignore if is not mutations (same as native)
			if pdb1_chain_seqpos_aa3s[ chain ][ seqpos ] == pdb2_chain_seqpos_aa3s[ chain ][ seqpos ]: continue
			# get single aa letter of pdb2 mut
			aa1_pdb2 = aa3_to_aa1[ pdb2_chain_seqpos_aa3s[ chain ][ seqpos ] ]	
			# add seqpos key if we dont have it yet
			if not mutmap.has_key( seqpos ):
				mutmap[ seqpos ] = {}
			if not mutmap[ seqpos ].has_key( aa1_pdb2 ):
				mutmap[ seqpos ][ aa1_pdb2 ] = 0
			# accumulate mutation into mutmap list for this key
			mutmap[ seqpos ][ aa1_pdb2 ] = mutmap[ seqpos ][ aa1_pdb2 ] + 1
	if not checked_any_pairs:
		print "ERROR: no overlapping chain,resi pairs in " + pdb1name, pdb2name
		sys.exit()
	return mutmap

def print_mut_mat( pdblist ):
	sys.stdout.write( '\t' )
	for pdb2name in pdblist:
		sys.stdout.write( pdb2name + '\t' )
	sys.stdout.write( '\n' )
	for pdb1name in pdblist:
		sys.stdout.write( pdb1name + '\t' )
		for pdb2name in pdblist:
			mut_data = gen_mut_data( pdb1name, pdb2name )
			for mut in mut_data:
				print mut,
			sys.stdout.write( '\t' )
		sys.stdout.write( '\n' )

def print_mut_list( pdblist, allvall, chain ):
	if allvall: ipdb_last = len( pdblist ) - 1
	else: ipdb_last = 1
	mutmap = {}
	for ipdb1 in range( ipdb_last ):
		for ipdb2 in range( ipdb1 + 1, len( pdblist ) ):
			pdb1name = pdblist[ ipdb1 ]
			pdb2name = pdblist[ ipdb2 ]
			mutmap_args = [ pdb1name, pdb2name, mutmap, chain ]
			add_mut_data_to_mutmap( mutmap_args )
			mutmap = mutmap_args[ 2 ]
	# print total over all pdb compares
	for numkey in mutmap.keys():
		sys.stdout.write( str( numkey ) + ':\t' )
		for aakey in mutmap[ numkey ].keys():
			sys.stdout.write( str( aakey ) + ":" + str( mutmap[ numkey ][ aakey ] ) + '\t' )
		sys.stdout.write( "\n" )
				

sys.argv.pop( 0 )
pdblist = sys.argv
if len( pdblist ) < 2:
	print "args:\tpdbname1\tpdbname2\t...\t<all_v_all?(f|t)>\tchainID(-)"
	sys.exit()

if pdblist[ -1 ] == '-':
  pdblist.pop()
  chain = False
else:
  chain = pdblist.pop()

if pdblist[ -1 ].lower() == 't':
	pdblist.pop()
	allvall = True
else:
	allvall = False
	if pdblist[ -1 ].lower() == 'f':
		pdblist.pop()
print_mut_list( pdblist, allvall, chain )

