#!/usr/bin/python

#################################################################

import os
import sys
import math

if( len( sys.argv ) < 2 ):
	print "args:\tanlfile <skipterm True||False>"
	sys.exit()
sys.argv.pop( 0 )
anlname = sys.argv.pop( 0 )
skipterm = False
if( len( sys.argv ) > 0 ):
	skipterm = sys.argv.pop( 0 )

anlfile = open( anlname, 'r' )
anl = anlfile.readlines()
matname = anlname[ 0:anlname.rfind( '.' ) ] + '.anlmat'
matfile = open( matname, 'w' )
keyname = anlname[ 0:anlname.rfind( '.' ) ] + '.anlkey'
keyfile = open( keyname, 'w' )
pdbsname = anlname[ 0:anlname.rfind( '.' ) ] + '.anlpdb'
pdbsfile = open( pdbsname, 'w' )

tag2idx = { 'rot_anl.nat:': 1,'rot_anl.min:': 2,'rot_anl.rtmin:': 3 }
taglist = [ 'rot_anl.nat:','rot_anl.min:','rot_anl.rtmin:' ]
aa2idx = { 'ALA': 1,'CYS': 2,'ASP': 3,'GLU': 4,'PHE': 5,'GLY': 6,'HIS': 7,'ILE': 8,'LYS': 9,'LEU': 10,'MET': 11,'ASN': 12,'PRO': 13,'GLN': 14,'ARG': 15,'SER': 16,'THR': 17,'VAL': 18,'TRP': 19,'TYR': 20 }
aalist = [ 'ALA','CYS','ASP','GLU','PHE','GLY','HIS','ILE','LYS','LEU','MET','ASN','PRO','GLN','ARG','SER','THR','VAL','TRP','TYR' ]

#skip termini
for i in range( 0, len( anl ) ):
	line = anl[ i ]
	line = line.rstrip()
	parse = line.split()

	if( skipterm ):
		#skip temrini
		#assumes tracer tags. pdbname must be elem 1 (not 0)!!
		if i < len( taglist ): continue
		if i >= ( len( anl ) - len( taglist ) ): continue
		pdb = parse[ 1 ].split( '.' )[ 0 ]
		lastpdb = anl[ i + len( taglist ) ].split()[ 1 ].split( '.' )[ 0 ]
		nextpdb = anl[ i - len( taglist ) ].split()[ 1 ].split( '.' )[ 0 ]
		if pdb != lastpdb: continue
		if pdb != nextpdb: continue

	matline = []
	keyline = [ 'tagidx:', 'aaidx:' ]
	for ii in range( 0, len( parse ) ):
		#rotbin screws this up!
		if parse[ ii ] == 'rotbin:':
			continue
		elif '.pdb' in parse[ ii ]:
			pdbsfile.write( parse[ ii ] + '\n' )
		elif parse[ ii ] in taglist:
			tag = parse[ ii ]
			matline.append( str( tag2idx[ tag ] ) )
		#ignoring chainres for now, it's in the pdb name anyway....
		elif parse[ ii ] in aalist:
			aa = parse[ ii ]
			matline.append( str( aa2idx[ aa ] ) )
		#need to handle chi's specially because variable number of chi's
		elif 'psi' in parse[ ii ]:
			matline.append( str( parse[ ii + 1 ] ) )
			#only write once, write at 4th line in case of ignore termini
			if i == len( taglist ): keyline.append( str( parse[ ii ] ) ) 
			#once we're at psi, print all chi's then bail out
			if ( len( parse ) - 1 ) >= ii + 3: matline.append( str( parse[ ii + 3 ] ) ) 
			else: matline.append( '0.0' ) 
			if ( len( parse ) - 1 ) >= ii + 5: matline.append( str( parse[ ii + 5 ] ) ) 
			else: matline.append( '0.0' ) 
			if ( len( parse ) - 1 ) >= ii + 7: matline.append( str( parse[ ii + 7 ] ) ) 
			else: matline.append( '0.0' ) 
			if ( len( parse ) - 1 ) >= ii + 9: matline.append( str( parse[ ii + 9 ] ) ) 
			else: matline.append( '0.0' ) 
			if i == len( taglist ): keyline.extend( [ 'chi1:', 'chi2:', 'chi3:', 'chi4:' ] ) 
			break
		elif ':' in parse[ ii ]:
			matline.append( str( parse[ ii + 1 ] ) )
			if i == len( taglist ): keyline.append( str( parse[ ii ] ) ) 
	matfile.write( ' '.join( matline ) + '\n' )
	if i == len( taglist ): keyfile.write( '\n'.join( keyline ) + '\n' )
