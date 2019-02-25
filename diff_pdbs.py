#!/usr/bin/python

import sys
import os

aa3_to_aa1 = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
              'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
              'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
              'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
              'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

#get dict of chain-->seqpos-->aa3 for a pdb
def get_chain_seqpos_aa3s( pdb ):
	chain_seqpos_aa3s = {}
	for line in pdb:
		if not ( len( line ) > 20 ): continue
		if not ( line[0:4] == 'ATOM' or (line[0:6] == 'HETATM') & (line[17:20]=='MSE') ): continue
		chain = line[ 21 ]
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

def gen_mut_data( pdb1name, pdb2name ):
	pdb1 = open( pdb1name, 'r' ).readlines()
	pdb2 = open( pdb2name, 'r' ).readlines()
	pdb1_chain_seqpos_aa3s = get_chain_seqpos_aa3s( pdb1 )
	pdb2_chain_seqpos_aa3s = get_chain_seqpos_aa3s( pdb2 )

	mut_data = []
	checked_any_pairs = False
	#save all elements of 2 dicts where aa3 doesn't match
	#skip if chain,seqpos isn't in pdb2
	for chain in sorted( pdb1_chain_seqpos_aa3s.iterkeys() ):
		if not( pdb2_chain_seqpos_aa3s.has_key( chain ) ): continue
		for seqpos in sorted( pdb1_chain_seqpos_aa3s[ chain ].iterkeys() ):
			if not( pdb2_chain_seqpos_aa3s[ chain ].has_key( seqpos ) ): continue
			checked_any_pairs = True
			if pdb1_chain_seqpos_aa3s[ chain ][ seqpos ] == pdb2_chain_seqpos_aa3s[ chain ][ seqpos ]: continue
			mut = str( seqpos ) + ' ' + chain + ' ' + pdb1_chain_seqpos_aa3s[ chain ][ seqpos ] + ' ' + '->' + ' ' + pdb2_chain_seqpos_aa3s[ chain ][ seqpos ]
#			mut = aa3_to_aa1[ pdb1_chain_seqpos_aa3s[ chain ][ seqpos ] ] + '_' + str( seqpos ) + chain + '_' + aa3_to_aa1[ pdb2_chain_seqpos_aa3s[ chain ][ seqpos ] ]
			mut_data.append( mut )
	if not checked_any_pairs:
		print "ERROR: no overlapping chain,resi pairs in " + pdb1name, pdb2name
		sys.exit()
	return mut_data

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

def print_mut_list( pdblist, allvall ):
	if allvall: ipdb_last = len( pdblist ) - 1
	else: ipdb_last = 1
	for ipdb1 in range( ipdb_last ):
		for ipdb2 in range( ipdb1 + 1, len( pdblist ) ):
			pdb1name = pdblist[ ipdb1 ]
			pdb2name = pdblist[ ipdb2 ]
			muts = gen_mut_data( pdb1name, pdb2name )
			print pdb1name, '->', pdb2name
			for mut in muts:
				print mut

sys.argv.pop( 0 )
pdblist = sys.argv
if len( pdblist ) < 2:
	print "args:\tpdbname1\tpdbname2\t...\t<all_v_all?(f|t)>"
	sys.exit()
if pdblist[ -1 ].lower() == 't':
	pdblist.pop()
	allvall = True
else:
	allvall = False
	if pdblist[ -1 ].lower() == 'f':
		pdblist.pop()
print_mut_list( pdblist, allvall )

