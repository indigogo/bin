#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tpdblist\tpdb_nums"
	sys.exit()
sys.argv.pop( 0 )
pdblistname = sys.argv.pop( 0 )
my_pdb_nums = sys.argv
istub = 0
pdblist = open( pdblistname, 'r' ).readlines()
for pdbname in pdblist:
	pdb = open( pdbname.rstrip(), 'r' ).readlines()
	ddg = '0.0'
	stubs = {}
	for line in pdb:
		line = line.rstrip()
		if line[ 0:4 ] == 'ATOM':
			chain = line[ 21 ]
			resnum = line[ 22:26 ].strip()
			pdb_num = resnum + chain
			if pdb_num not in my_pdb_nums: continue
			stubs.setdefault( pdb_num, [] ).append( line )
		elif line[ 0:3 ] == 'ddg':
			ddg = line.split()[ 1 ]
	for stub in stubs.values():
		istub += 1
		print 'MODEL S_0000000' + str( istub )
		print 'REMARK 221 ' + str( ddg )
		for line in stub: print line
		print 'TER'
		print 'ENDMDL'

