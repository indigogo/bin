#!/usr/bin/python

#####this will compare atom pair distance in 2 ref_pdb sets######
# for each ref_pdb:
# 1.load ref_pdbs	
# 2.loop over atompairs	by lines
# 3.get rosetta atomtypes, print them
# optional filter by distance, or interface
# THIS IGNORES RESIDUE W/ <=2 SEQ SEP!
#################################################################

# this whole thing could be faster if we cached interface distances
# when we checked them, though we're onyl recalculating counting
# N(interface atoms) distances

import os
import sys
import math

#functions and lookup tables
def get_atom_dist( a1, a2 ):
	dist = math.sqrt( ( float( a1[ 30:38 ] ) - float( a2[ 30:38 ] ) )**2 + ( float( a1[ 38:46 ] ) - float( a2[ 38:46 ] ) )**2 + ( float( a1[ 46:54 ] ) - float( a2[ 46:54 ] ) )**2 )
	return dist
def atom_is_interface( pdb, iatom, cutoff, is_interface_atom ):
	if is_interface_atom[ iatom ]: return True
	atom1 = pdb[ iatom ]
	chain1 = atom1[ 21 ]
	for jatom in range( len( pdb ) ):
		atom2 = pdb[ jatom ]
		if atom2[ 21 ] == chain1: continue
		if get_atom_dist( atom1, atom2 ) < cutoff:
			is_interface_atom[ iatom ] = True
			is_interface_atom[ jatom ] = True
			return True
			break
	return False
def clean_pdb( pdb ):
	pdb_clean = []
	for iline in range( len( pdb ) ):
		line = pdb[ iline ]
		if line[ 0:4 ] == 'ATOM' or line[ 0:6 ] == 'HETATM': pdb_clean.append( line )
	return pdb_clean

aas = [ 'ALA', 'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN', 'PRO', 'GLN', 'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR' ]
mainchain_atoms = [ ' N  ', ' CA ', ' C  ', ' O  ' ]

if( len( sys.argv ) < 3 ):
	print "args:\tref_pdblist\ttest_pdblist\t<nbr_cutoff>\t<prot-prot||prot-other>"
	sys.exit()
sys.argv.pop( 0 )
ref_pdblist_name = sys.argv.pop( 0 )
test_pdblist_name = sys.argv.pop( 0 )
if len( sys.argv ) > 0:
	cutoff = float( sys.argv.pop( 0 ) )
else: cutoff = False
if len( sys.argv ) > 0:
	interface = sys.argv.pop( 0 )
else: interface = False

incl_other = False
ignore_other_bb = False
prot_other_interface_only = False
if interface == 'other-prot' :  prot_other_interface_only = True 

ref_pdblist = open( ref_pdblist_name, 'r' ).readlines()
test_pdblist = open( test_pdblist_name, 'r' ).readlines()

#check lists are same length
#TODO ref ref_pdblist can be shorter if exactly n test ref_pdbs for each ref?
if len( ref_pdblist ) != len( test_pdblist ):
	print "ERROR:\tpdblist length mismatch!\n"
	sys.exit()

#over each ref_pdb in lists
for ipdb in range( len( test_pdblist ) ):

	#load pdbs
	ref_pdbname = ref_pdblist[ ipdb ].rstrip()
	ref_pdb = open( ref_pdbname, 'r' ).readlines()
	test_pdbname = test_pdblist[ ipdb ].rstrip()
	test_pdb = open( test_pdbname, 'r' ).readlines()

	#clean them
	ref_pdb = clean_pdb( ref_pdb )
	test_pdb = clean_pdb( test_pdb )
	#same number atoms?
	if len( ref_pdb ) != len( test_pdb ):
		print "ERROR:\tpdb length mismatch: " + ref_pdbnameb + " " + test_pdbname + "!\n"
		sys.exit()

	#interface filter
	is_interface_atom = [ False ] * len( ref_pdb )

	#iter over all atoms
	#up to second to last atom, because i < j (no double counting pairs)
	#warning! must reiter over all if we skip nonprot atoms in i!
	for i in range( len( ref_pdb ) - 1 ):
		ref_atm1 = ref_pdb[ i ]
		ref_resi1 = ref_atm1[ 22:26 ]
		ref_chain1 = ref_atm1[ 21 ]
		ref_resn1 = ref_atm1[ 17:20 ]
		ref_atmn1 = ref_atm1[ 12:16 ]

		#ref_resn = ref_atm1[ 17:20 ]
		#if not ( ref_resn in aas ): continue

		#is interface atom? array prevents double-checking
		if interface:
			if not atom_is_interface( ref_pdb, i, cutoff, is_interface_atom ):
				continue

		for j in range( i + 1, len( ref_pdb ) ):
			ref_atm2 = ref_pdb[ j ]
			ref_resi2 = ref_atm2[ 22:26 ]
		 	ref_chain2 = ref_atm2[ 21 ]
			ref_resn2 = ref_atm2[ 17:20 ]
			ref_atmn2 = ref_atm2[ 12:16 ]

			#skip if i->i+2 in residue sequence
			if ref_chain1 == ref_chain2:
				if abs( int( ref_resi1 ) - int( ref_resi2 ) ) <= 2:
					continue

			#interface only?
			if interface:
				if not atom_is_interface( ref_pdb, j, cutoff, is_interface_atom ):
					continue

			ref_dist = get_atom_dist( ref_atm1, ref_atm2 )
			#skip if dist >= cutoff
			if cutoff and ref_dist >= cutoff: continue

			#all filters passed, get rest of output data and print

			test_atm1 = test_pdb[ i ]
			test_atm2 = test_pdb[ j ]
			test_dist = get_atom_dist( test_atm1, test_atm2 )

			#print ref_resn1, ref_atmn1, ref_resn2, ref_atmn2, ref_dist, test_dist
			print ref_resn1, ref_resi1, ref_atmn1, ref_resn2, ref_resi2, ref_atmn2, ref_dist, test_dist
