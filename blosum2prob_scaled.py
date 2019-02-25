#!/usr/bin/python

import sys
import os
import math

aa_types = 'XACDEFGHIKLMNPQRSTVWY'
aa2idx = dict( zip( aa_types, range( 0, len( aa_types ) ) ) )
def load_mat( filename ):
	file = open( filename, 'r' ).readlines()
	#format hardcoded, line 0 = comments, line 1 = col labels, symmetric
	col_aas_in = file[ 1 ].rstrip().split()
	#dict of aa letter -> substitution score vector
	scmat = {}
	min_val = None
	max_val = None
	for il in range( 2, len( file ) ):
		line = file[ il ]
		toks = line.rstrip().split()
		row_aa = toks[ 0 ]
		#is this row label in our allowed aa_types?
		if row_aa not in aa_types: continue
		scmat[ row_aa ] = {}
		for itok in range( 1, len( toks ) ):
			#what is the colum label for this value?
			col_aa = col_aas_in[ itok - 1 ]
			#is this column label in our allowed aa_types?
			if col_aa not in aa_types: continue
			val = float( toks[ itok ] )
			scmat[ row_aa ][ col_aa ] = val
			if min_val is None or val < min_val: min_val = val
			if max_val is None or val > max_val: max_val = val
	return scmat, min_val, max_val

## USE P = 1/( 1 + exp( -1 * X ) ) to scale blosum scores to probabilities 
def score2prob( score ):
	prob = 1 / ( 1 + math.exp( -1 * float( score ) ) )
	return prob

#parses iedb data into libsvm format, transforms sequence into feature vector, each aa is a blosum row
sys.argv.pop( 0 )
try:
	mat_filename = sys.argv.pop( 0 )
except:
	print "args:\tiedb_data\tseq_col\tval_col(-)\tblosum_mat"
	sys.exit()

scmat, min_score, max_score = load_mat( mat_filename )
#min_prob = score2prob( min_score )
#max_prob = score2prob( max_score )
#print col keys
sys.stdout.write( '\t' )
for col_aa in sorted( scmat[ aa_types[ 1 ] ].iterkeys() ): sys.stdout.write( col_aa + '\t' )
sys.stdout.write( '\n' )
for row_aa in sorted( scmat.iterkeys() ):
	sys.stdout.write( row_aa + '\t' )
	for col_aa in sorted( scmat[ row_aa ].iterkeys() ):
		#rescale from [0,1] to [-1,1]
		prob_scaled = 2 * score2prob( scmat[ row_aa ][ col_aa ] ) - 1.
		sys.stdout.write( '%.3f' % prob_scaled + '\t' ) 
	sys.stdout.write( '\n' )

