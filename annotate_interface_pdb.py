#!/usr/bin/python

#####this is going to annotate pdbs for interface residues#######
# 1.load pdb							#
# 2.loop over res, skip non-prot, ala, gly			#
# 3.inner nbr loop, skip if is self chain			#
# 4.nbr=true if sc atom of i within cutoff of any j atom	#
#################################################################

import os
import sys
import math

if( len( sys.argv ) < 3 ):
	print "args:\tpdbfile\tnbr_cutoff"
	sys.exit()
sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
cutoff = float( sys.argv.pop( 0 ) )
incl_dna = False
prot_nonprot_interface_only = True

def get_atom_dist( a1, a2 ):
	dist = math.sqrt( ( float( a1[ 30:38 ] ) - float( a2[ 30:38 ] ) )**2 + ( float( a1[ 38:46 ] ) - float( a2[ 38:46 ] ) )**2 + ( float( a1[ 46:54 ] ) - float( a2[ 46:54 ] ) )**2 )
	return dist

pdbfile = open( pdbname, 'r' )
pdb = pdbfile.readlines()
newpdbname = pdbname[ 0:( len( pdbname ) - 3 ) ] + 'annot.pdb'
newpdbfile = open( newpdbname, 'w' )

aas = [ 'ALA', 'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN', 'PRO', 'GLN', 'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR' ]
mainchain_atoms = [ ' N  ', ' CA ', ' C  ', ' O  ' ]

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

			#over all cached res lines
			for scline in reslines:
				#check if mainchain or sc
				if ( scline[ 12:16 ] in mainchain_atoms ): continue
				#check distance
				if get_atom_dist( scline, nbrline ) < cutoff:
					is_interface = True
					remark = 'REPACK ' + scline[ 22:26 ] + '  ' + scline[ 21 ] + '\n'
					newpdbfile.write( remark )
					break

			if is_interface: break
		
		#clear sc cache
		is_interface = False
		reslines = []
	
	reslines.append( line )
	last_chainres = chainres

newpdbfile.writelines( pdb )
pdbfile.close()
newpdbfile.close()

