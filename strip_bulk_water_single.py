#!/usr/bin/python

import sys
import os
import math

#only print water res if has an atom within nbr cutoff

if( len( sys.argv ) < 2 ):
	print "args:\tpdbfile\tnbr_cutoff"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
nbr_cutoff = float( sys.argv.pop( 0 ) )

soltypes = [ 'WAT', 'SOL', 'TP3', 'TP5', 'HOH' ]

def get_atom_dist( a1, a2 ):
	dist = math.sqrt( ( float( a1[ 30:38 ] ) - float( a2[ 30:38 ] ) )**2 + ( float( a1[ 38:46 ] ) - float( a2[ 38:46 ] ) )**2 + ( float( a1[ 46:54 ] ) - float( a2[ 46:54 ] ) )**2 )
	return dist

name = '.'.join( filename.split( '.' )[ :-1 ] )
pdbout = open( name + '.shell.pdb', 'w' )
file = open( filename, 'r' ).readlines()

iatom = -1
while iatom < len( file ) - 1:
	iatom += 1
	atom = file[ iatom ]
	#ignore non coord atoms
	if atom[ 0:4 ] != 'ATOM' and atom[ 0:6 ] != 'HETATM': continue
	resn = atom[ 17:20 ]
	#if water res, cache whole res
	if resn in soltypes:
		water = file[ iatom:( iatom+3 ) ]
		is_nbr = False
		#see if is a nbr water
		for jatom in range( len( file ) ):
			nbr_atom = file[ jatom ]
			if nbr_atom[ 0:4 ] != 'ATOM' and nbr_atom[ 0:6 ] != 'HETATM': continue
			nbr_resn = nbr_atom[ 17:20 ]
			if nbr_resn in soltypes: continue
			for wateratom in water:
				if get_atom_dist( wateratom, nbr_atom ) <= nbr_cutoff:
					is_nbr = True
					break
			if is_nbr: break
		if is_nbr:
			for wateratom in water:
				#replace SPC water names w/ TP3 names for rosetta input
				wateratom = wateratom.replace( 'SOL', 'TP3' )
				wateratom = wateratom.replace( 'OW', 'O ' )
				wateratom = wateratom.replace( 'HW1', 'H1 ' )
				wateratom = wateratom.replace( 'HW2', 'H2 ' )
				pdbout.write( wateratom )
		#increment iter because we checked all three water atoms
		iatom += 2
	#if not water res, print
	else: pdbout.write( atom )
	
