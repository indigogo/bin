#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\t"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )

scoreterms = [ 'BackHbond', 'SideHbond', 'Energy_VdW', 'Electro', 'Energy_SolvP', 'Energy_SolvH', 'Energy_vdwclash', 'energy_torsion', 'backbone_vdwclash', 'Entropy_sidec', 'Entropy_mainc', 'water bonds', 'helix dipole', 'loop_entropy', 'cis_bond', 'disulfide', 'kn electrostatic', 'partial covalent interactions', 'Energy_Ionisation', 'Entropy Complex', 'Total']

#load output from foldx scoring
file = open( filename, 'r' ).readlines()
reading_native = True
natscore = [None] * len( scoreterms )
decoyscore_davg = [0] * len( scoreterms )
ndecoy = 0;
for i in range( len( file ) ):
	line = file[ i ]
	line = line.rstrip()
	parse = line.split( '=' )
	if len( parse ) < 0:
		print line
		continue
	term = parse[ 0 ]
	term = term.lstrip()
	term = term.rstrip()
	#if is a scoreterm line
	if term in scoreterms:
		val = parse[ 1 ]
		val = val.lstrip()
		val = val.rstrip()
		#load native scores if is first model, otherwise diff them and add dscore to output
		scoreidx = scoreterms.index( term )
		if reading_native:
			natscore[ scoreidx ] = val
			if term == "Total": reading_native = False
			print line
			continue
		else:
			dval = float( val ) - float( natscore[ scoreidx ] )
			print line + "\t" + str( dval )
			if term == "Total": ndecoy +=1	
			decoyscore_davg[ scoreidx ] += dval
			continue
	print line

for i in range( len( decoyscore_davg ) ):
	decoyscore_davg[ i ] = decoyscore_davg[ i ] / ndecoy

print "\n\n\t\t<***Average Deltas***>\t\t\n\n"
for term in scoreterms:
	print "<d( " + term + " )>\t=\t" + str( decoyscore_davg[ scoreterms.index( term ) ] )
