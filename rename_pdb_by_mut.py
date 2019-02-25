#!/usr/bin/python

import sys
import os
from shutil import copyfile

aa3_to_aa1 = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
              'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
              'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
              'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
              'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

#get dict of chain-->seqpos-->aa1 for a pdb
def get_chain_seqpos_aa1s( pdb, use_chain ):
	chain_seqpos_aa1s = {}
	for line in pdb:
		if not ( len( line ) > 20 ): continue
		if not ( line[0:4] == 'ATOM' or (line[0:6] == 'HETATM') & (line[17:20]=='MSE') ): continue
		chain = line[ 21 ]
		if chain == ' ': chain = '_'
		if use_chain != False and chain != use_chain:
			continue
		seqpos = int( line[23:26].strip() )
		try:
			aa1 = aa3_to_aa1[ line[17:20].strip() ]
		except:
			aa1 = 'X'
		#init this chain key if not isdef
		if not chain_seqpos_aa1s.has_key( chain ):
			chain_seqpos_aa1s[ chain ] = {}
		#skip if we've already stored this chain,seqpos aa1
		elif chain_seqpos_aa1s[ chain ].has_key( seqpos ): continue
		chain_seqpos_aa1s[ chain ][ seqpos ] = aa1
	return chain_seqpos_aa1s

def gen_mut_data( pdb1name, pdb2name, chain ):
	pdb1 = open( pdb1name, 'r' ).readlines()
	pdb2 = open( pdb2name, 'r' ).readlines()
	pdb1_chain_seqpos_aa1s = get_chain_seqpos_aa1s( pdb1, chain )
	pdb2_chain_seqpos_aa1s = get_chain_seqpos_aa1s( pdb2, chain )

	mut_data = []
	checked_any_pairs = False
	#save all elements of 2 dicts where aa1 doesn't match
	#skip if chain,seqpos isn't in pdb2
	for chain in sorted( pdb1_chain_seqpos_aa1s.iterkeys() ):
		if not( pdb2_chain_seqpos_aa1s.has_key( chain ) ): continue
		for seqpos in sorted( pdb1_chain_seqpos_aa1s[ chain ].iterkeys() ):
			if not( pdb2_chain_seqpos_aa1s[ chain ].has_key( seqpos ) ): continue
			checked_any_pairs = True
			if pdb1_chain_seqpos_aa1s[ chain ][ seqpos ] == pdb2_chain_seqpos_aa1s[ chain ][ seqpos ]: continue
			# add string to list e.g. "A_S456M"
			# TODO: if chain specified, leave off chain ID
			if chain is False:
				mut = chain + '_' + pdb1_chain_seqpos_aa1s[ chain ][ seqpos ] + str( seqpos ) + pdb2_chain_seqpos_aa1s[ chain ][ seqpos ]
			else:
				mut = pdb1_chain_seqpos_aa1s[ chain ][ seqpos ] + str( seqpos ) + pdb2_chain_seqpos_aa1s[ chain ][ seqpos ]
			mut_data.append( mut )
	if not checked_any_pairs:
		print "ERROR: no overlapping chain,resi pairs in " + pdb1name, pdb2name
		sys.exit()
	return mut_data

def print_mut_list( pdblist, allvall, chain ):
	if allvall: ipdb_last = len( pdblist ) - 1
	else: ipdb_last = 1
	for ipdb1 in range( ipdb_last ):
		for ipdb2 in range( ipdb1 + 1, len( pdblist ) ):
			pdb1name = pdblist[ ipdb1 ]
			pdb2name = pdblist[ ipdb2 ]
			muts = gen_mut_data( pdb1name, pdb2name, chain )

#			print pdb1name, '->', pdb2name
			new_pdb2name = os.path.splitext( os.path.basename( pdb1name ) )[ 0 ]
			for mut in muts:
				new_pdb2name = new_pdb2name + '+' + mut
			new_pdb2name = new_pdb2name + '.pdb'
			if not os.path.isfile( new_pdb2name ):
				os.rename( pdb2name, new_pdb2name )



#TODO: swirch to args parser
# this argument list setup is backwards so that arbitrary pdb filenames can be passed as arguments in cmdline
sys.argv.pop( 0 )
pdblist = sys.argv
if len( pdblist ) < 2:
	print "args:\tpdbname1\tpdbname2\t...\tall_v_all?(f|t)\tchainID(-)"
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

