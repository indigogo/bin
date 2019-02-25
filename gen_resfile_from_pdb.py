#!/usr/bin/python

#####        read annotated pdbs, gen resfiles           #######
#################################################################

import os
import sys
import math

if( len( sys.argv ) < 2 ):
	print "args:\tpdbfile"
	sys.exit()
sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )

pdbfile = open( pdbname, 'r' )
pdb = pdbfile.readlines()
remark = 'REPACK'

resfilename = pdbname[ 0:( len( pdbname ) - 3 ) ] + 'resfile'
resfile = open( resfilename, 'w' )
resfile.write( 'NATRO\n' )
resfile.write( 'start\n' )

for i in range( len( pdb ) ):
	if not pdb[ i ].startswith( remark ): continue
	line = pdb[ i ]
	line = line.rstrip()

	res = []

	parse = line.split()
	parse.pop( 0 )
	parse.append( 'NATAA\n' )
	resfile.write( ' '.join( parse )  )

pdbfile.close()
resfile.close()

