#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
except:
	print "args:\tpdblist(-)\t<all(f|t)>"
	sys.exit()
try:
	all = sys.argv.pop( 0 )
	if all.lower()[ 0 ] == 't': all = True
	else: all = False
except:
	all = False

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

for i1 in range( len( file ) - 1 ):
	pdb1 = file[ i1 ].rstrip()
	#skip if we've already removed this guy
	if not os.path.exists( pdb1 ): continue
	for i2 in range( (i1 + 1), len( file ) ):
		pdb2 = file[ i2 ].rstrip()
		if not os.path.exists( pdb2 ): continue
		if pdb1 == pdb2: continue
		diff = os.popen( 'diff_pdbs.py ' + pdb1 + ' ' + pdb2 ).readlines()
		if len( diff ) == 1:
			print 'Duplicate sequence pdbs!', pdb1, pdb2
			if all: os.system( 'rm *' + '.'.join( pdb2.split( '.' )[ :-1 ] ) + '.*' )  
			else: os.system( 'rm ' + pdb2 )
