#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tcollect_distribution_stdout\tn_dim"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
n_dim = int( sys.argv.pop( 0 ) )

file = open( filename, 'r' ).readlines()
atomvals = {}
n_atomvals = {}
for line in file:
	line = line.rstrip()
	parse = line.split()
	if parse[ 0 ] != 'pilot.chrisk.collect_distribution:' or parse[ 1 ] == 'collecting':
		continue
	#get resi_atom
	#!!!col numbers will change!!!
	resi_atom = ' '.join( [ parse[ 6 ], parse[ 7 ] ] )
	#iter over n_dim from end and store vals
	vals = []
	for ival in range( -1 * n_dim, 0 ):
		vals.append( float( parse[ ival ] ) )
	#if key exists, add to sum, else create new entry
	if resi_atom in atomvals.keys():
		for ival in range( 0, n_dim ):
			atomvals[ resi_atom ][ ival ] += vals[ ival ]
			n_atomvals[ resi_atom ] += 1
	else:
			atomvals[ resi_atom ] =  vals
			n_atomvals[ resi_atom ] =  1

for resi_atom, vals in atomvals.iteritems():
	for ival in range( 0, n_dim ):
		atomvals[ resi_atom ][ ival ] = atomvals[ resi_atom ][ ival ] /  n_atomvals[ resi_atom ]
for resi_atom, vals in sorted( atomvals.iteritems() ):
	print resi_atom, '\t',
	for ival in range( 0, n_dim ):
		print float( vals[ ival ] ), '\t',
	print
