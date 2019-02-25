#!/usr/bin/python

# this turns a pssm into a bunch of random seqs
# using seq position identity probabilities
# weighted linearly by score values at each position

import sys
import os
import random

if( len( sys.argv ) < 2 ):
	print "args:\tpssm\tn_seqs"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
n_seqs = int( sys.argv.pop( 0 ) )

file = open( filename, 'r' ).readlines()
length = None
aa2scores = {}
aas = []
for line in file:
	line = line.split()
	if line[ 0 ][ 0 ] == '#': continue #skip comments
	aa = line.pop( 0 ) #rest of line is vals
	aas.append( aa )
	#init length, else die if inconsistent
	if length is None: length  = len( line )
	elif length != len( line ):
		print "inconsistent N entries at aa " + aa
		sys.exit()
	#store vals, needs conv to floats
	vals = []
	for val in line:
		val = float( val )
		vals.append( val )
	aa2scores[ aa ] = vals

#xform vals to cumsum 
cumsums = []
for iseq in range( length ):
	#shift to [0,max] so cumsum isnt screwed up!
	min = 0
	for aa in aa2scores.keys():
		if aa2scores[ aa ][ iseq ] < min: min = aa2scores[ aa ][ iseq ]
	for aa in aa2scores.keys():
		aa2scores[ aa ][ iseq ] = aa2scores[ aa ][ iseq ] - min

	#xform vals to cumulative sums over each position
	cumsum = 0
	for aa in aa2scores.keys():
		cumsum += aa2scores[ aa ][ iseq ]
		aa2scores[ aa ][ iseq ] = cumsum
	cumsums.append( cumsum )

#gen seqs
for iline in range( n_seqs ):
	# now pick rand aa's for each position of each seq wtd by vals in aa2scores
	for iseq in range( length ):
		if cumsums[ iseq ] == 0:
			aa = random.choice( aas )
			sys.stdout.write( aa )
			continue
		rand_res_val = random.random() * cumsums[ iseq ]
		for aa in aa2scores.keys():
			if rand_res_val <= aa2scores[ aa ][ iseq ]:
				sys.stdout.write( aa )
				break
	print
