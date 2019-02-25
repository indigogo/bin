#!/usr/bin/python

#####        read annotated pdfbs, gen resfiles           #######
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

n = 0
for i in range( len( pdb ) ):
	if not pdb[ i ].startswith( remark ): continue
	line = pdb[ i ]
	line = line.rstrip()

	res = []
	n+=1

	parse = line.split()
	parse.pop( 0 )
	res.append( 'NATRO\n' )
	res.append( 'start\n' )
	for j in range( 0, len( parse ), 2 ):
			res.append( parse[ j ] + ' ' + parse[ j + 1 ] + ' NATAA\n' )


	resfilename = pdbname[ 0:( len( pdbname ) - 3 ) ] + repr(n) + '.resfile'
	resfile = open( resfilename, 'w' )
	resfile.writelines( res )
	resfile.close()

pdbfile.close()

