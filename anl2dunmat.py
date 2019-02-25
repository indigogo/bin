#!/usr/bin/python

#################################################################

import os
import sys
import math

if( len( sys.argv ) < 2 ):
	print "args:\tanlfile <skipterm True||False>"
	print "aaidx phi psi chi1 chi2 chi3 chi4"
	sys.exit()
sys.argv.pop( 0 )
anlname = sys.argv.pop( 0 )
skipterm = False
if( len( sys.argv ) > 0 ):
	skipterm = sys.argv.pop( 0 )

anlfile = open( anlname, 'r' )
anl = anlfile.readlines()

aa2idx = { 'ALA': 1,'CYS': 2,'ASP': 3,'GLU': 4,'PHE': 5,'GLY': 6,'HIS': 7,'ILE': 8,'LYS': 9,'LEU': 10,'MET': 11,'ASN': 12,'PRO': 13,'GLN': 14,'ARG': 15,'SER': 16,'THR': 17,'VAL': 18,'TRP': 19,'TYR': 20 }
aalist = [ 'ALA','CYS','ASP','GLU','PHE','GLY','HIS','ILE','LYS','LEU','MET','ASN','PRO','GLN','ARG','SER','THR','VAL','TRP','TYR' ]

#skip termini
if( skipterm ):
	anl.pop( 0 )
	anl.pop()
for i in range( 0, len( anl ) ):
	line = anl[ i ]
	line = line.rstrip()
	parse = line.split()

	if( skipterm ):
		#skip temrini
		#assumes no tracer tags. pdbname must be elem 0!!
		pdb = parse[ 0 ].split( '.' )[ 0 ]
		lastpdb = anl[ i + 1 ].split()[ 0 ].split( '.' )[ 0 ]
		nextpdb = anl[ i - 1 ].split()[ 0 ].split( '.' )[ 0 ]
		if pdb != lastpdb: continue
		if pdb != nextpdb: continue

	phi = psi = chi1 = chi2 = chi3 = chi4 = '0.0'
	for ii in range( 0, len( parse ) ):
		if parse[ ii ] in aalist:
			aa = parse[ ii ]
			aaidx = str( aa2idx[ aa ] )
		if parse[ ii ] == 'phi:': phi = str( parse[ ii + 1] )
		if parse[ ii ] == 'psi:': psi = str( parse[ ii + 1] )
		if parse[ ii ] == 'chi1:': chi1 = str( parse[ ii + 1] )
		if parse[ ii ] == 'chi2:': chi2 = str( parse[ ii + 1] )
		if parse[ ii ] == 'chi3:': chi3 = str( parse[ ii + 1 ] )
		if parse[ ii ] == 'chi4:': chi4 = str( parse[ ii + 1 ] )
	outline = [ aaidx, phi, psi, chi1, chi2, chi3, chi4 ]
	print ' '.join( outline )
