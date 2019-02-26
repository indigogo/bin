#!/usr/bin/python

import os
import sys

if( len( sys.argv ) < 2 ):
	print "args:\tpdbfile\t<incl_hetatms(T|F)>"
	sys.exit()
sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
try:
	incl_hetatms = sys.argv.pop( 0 ).lower()
	if incl_hetatms == 't':
		incl_hetatms = True
	else:
		incl_hetatms = False
except:
 	incl_hetatms = False


pdbfile = open( pdbname, 'r' )
pdb = pdbfile.readlines()
chain_ids = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz')

name = '.'.join( pdbname.split('.')[ :-1 ] )
pdbout = open( name + '.mod2ch.pdb', 'w' )

chain = chain_ids.pop( 0 )
first_line = True
first_model = True
this_model = ''
last_model = this_model
pdb_modelchains = []
for i in range( len( pdb ) ):
	line = pdb[ i ]
	line = line.rstrip()
	if line[ 0:5 ].startswith( 'MODEL' ):
		this_model = line
	
	if incl_hetatms == True:
		if not ( line[ 0:4 ].startswith( 'ATOM' ) or line[ 0:6 ].startswith( 'HETATM' ) ): continue
	else:
		if not ( line[ 0:4 ].startswith( 'ATOM' ) ): continue

	this_chain = line[ 21 ]
	if first_line:
		pdb_modelchains.append( ( this_model, this_chain ) )
	if not first_line:
		if ( this_model, this_chain ) not in pdb_modelchains:
			pdb_modelchains.append( ( this_model, this_chain ) )
			try:
				chain = chain_ids.pop( 0 )
			except:
				print( 'ERROR: Too many chains, we ran out of valid characters to assign as chain IDs!!\n' )
				sys.exit()
	else: first_line = False
	pdbout.write( line[ :21 ] + chain + line[ 22: ] + '\n' )

