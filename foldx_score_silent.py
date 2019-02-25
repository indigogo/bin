#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tsilentfile\ttaglist"
	sys.exit()
sys.argv.pop( 0 )
silentfilename = sys.argv.pop( 0 )
if len( sys.argv ) > 0: tagfilename = sys.argv.pop( 0 )
else: tagfilename = 0

if tagfilename: tagfile = open( tagfilename, 'r' ).readlines()
else:
	silentfile = open( silentfilename, 'r' ).readlines()
	tagfile = []
	for silentline in silentfile:
		parse = silentline.split()
		if parse[ 0 ] == 'SCORE:' and parse[ 1 ] != 'score':
			tagfile.append( parse[ len( parse ) - 1 ] )
pdblist = open( 'pdblist', 'w' )

minicall = '~/trunk/mini/bin/extract_pdbs.linuxgccrelease -database ~/trunk/minirosetta_database -in:file:silent ' + silentfilename 
if tagfilename: minicall += ' -in:file:fullatom -tags '
for tag in tagfile:
	tag = tag.rstrip( '\n' )
	if tagfilename: minicall += tag + ' '
	pdblist.write( tag + '.pdb\n' )
pdblist.close()

#print minicall
os.system( minicall )

if tagfilename == 0: tagfilename = 'all'
foldx_basetext = open( 'score.fxin', 'r' ).readlines()
foldx_runfile = open( tagfilename + '.fxin', 'w' )
for i in range( 5 ):
	foldx_runfile.write( foldx_basetext[ i ] )
foldx_runfile.write( '<Stability>' + tagfilename + '.fxout;\n' )
for i in range( 6, len( foldx_basetext ) ):
	foldx_runfile.write( foldx_basetext[ i ] )
foldx_runfile.close()

foldxcall = '~/foldx/foldx -runfile ' + tagfilename + '.fxin'
os.system( foldxcall )
for tag in tagfile:
	tag = tag.rstrip( '\n' )
	os.system( 'rm ' + tag + '.pdb' )
