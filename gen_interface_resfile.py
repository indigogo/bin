#!/usr/bin/python

#####this is going to make a resfile for interface residues######
# 1.load pdb							#
# 2.loop over res, skip non-prot, ala, gly			#
# 3.inner nbr loop, skip if is self chain			#
# 4.nbr=true if sc atom of i within cutoff of any j atom	#
#################################################################

import os
import sys
import math

if( len( sys.argv ) < 3 ):
	print "args:\tpdbfile\tnbr_cutoff\t<dna-prot||prot-prot>"
	sys.exit()
sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
cutoff = float( sys.argv.pop( 0 ) )
inter_type = sys.argv.pop( 0 )

incl_dna = False
ignore_dna_bb = True
prot_nonprot_interface_only = False
if inter_type == 'dna-prot' :  prot_nonprot_interface_only = True 

def get_atom_dist( a1, a2 ):
	dist = math.sqrt( ( float( a1[ 30:38 ] ) - float( a2[ 30:38 ] ) )**2 + ( float( a1[ 38:46 ] ) - float( a2[ 38:46 ] ) )**2 + ( float( a1[ 46:54 ] ) - float( a2[ 46:54 ] ) )**2 )
	return dist

pdbfile = open( pdbname, 'r' )
pdb = pdbfile.readlines()
resfilename = pdbname[ 0:( len( pdbname ) - 3 ) ] + 'resfile'
resfile = open( resfilename, 'w' )
resfile.write( 'NATRO\n' )
resfile.write( 'start\n' )


aas = [ 'ALA', 'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN', 'PRO', 'GLN', 'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR' ]
mainchain_atoms = [ ' N  ', ' CA ', ' C  ', ' O  ' ]
#dna_bb_atoms = [ ' P ', ' OP1 ', ' OP2 ', ' O5\* ', ' C5\* ', ' C4\* ', ' O4\* ', ' C3\* ', ' O3\* ', ' C2\* ', ' C1\* ', ' O5\' ', ' C5\' ', ' C4\' ', ' O4\' ', ' C3\' ', ' O3\' ', ' C2\' ', ' C1\' ' ]
dna_bb_atoms=["P","OP1","OP2","O1P","O2P","O5*","C5*","C4*","O4*","C3*","O3*","C2*","C1*","O5'","C5'","C4'","O4'","C3'","O3'","C2'","C1'"]


last_chainres = ''
reslines = []
is_interface = False
for i in range( len( pdb ) ):
	#skip hetatms, hydrogens, non-prot
	line = pdb[ i ]
	line = line.rstrip()
	if not line[ 0:4 ].startswith( 'ATOM' ): continue
	if line[ 13 ] == 'H': continue
	if not ( line[ 17:20 ] in aas ): continue

	#if new residue, run search for previous res, then clear sc line cache
	chainres = line[ 21:26 ]
	if i > 0 and len( last_chainres ) > 0 and ( chainres != last_chainres or i == len( pdb ) ):

		#run search over all residues
		for j in range( len( pdb ) ):
			#skip hetatms, hydrogens, same chain
			nbrline = pdb[ j ]
			nbrline = nbrline.rstrip()
			if not nbrline[ 0:4 ].startswith( 'ATOM' ): continue
			if nbrline[ 13 ] == 'H': continue
			if nbrline[ 21 ] == last_chainres[ 0 ]: continue
			if prot_nonprot_interface_only and ( nbrline[ 17:20 ] in aas ): continue
			if ignore_dna_bb and ( nbrline[ 12:16 ].strip() in dna_bb_atoms ): continue

			#over all cached res lines
			for scline in reslines:
				#check if mainchain or sc
				if ( scline[ 12:16 ] in mainchain_atoms ): continue
				#check distance
				if get_atom_dist( scline, nbrline ) < cutoff:
					is_interface = True
					resline = scline[ 22:26 ].strip() + '  ' + scline[ 21 ] + ' NATAA\n'
					resfile.write( resline )
					break

			if is_interface: break
		
		#clear sc cache
		is_interface = False
		reslines = []
	
	reslines.append( line )
	last_chainres = chainres

pdbfile.close()
resfile.close()

