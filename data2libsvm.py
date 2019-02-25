#!/usr/bin/python

import sys
import os
import math

aa_types = 'ACDEFGHIKLMNPQRSTVWXY-'
aa2idx = dict( zip( aa_types, range( 0, len( aa_types ) ) ) )

def load_pssm( pssmfile ):
	pssm_length = None
	aa2scores = {}
	aas = []
	for line in pssmfile:
		line = line.split()
		if line[ 0 ][ 0 ] == '#': continue #skip comments
		aa = line.pop( 0 ) #rest of line is vals
		aas.append( aa )
		#init pssm_length, else die if inconsistent
		if pssm_length is None: pssm_length  = len( line )
		elif pssm_length != len( line ):
			print "inconsistent N entries at aa " + aa
			sys.exit()
		#store vals, needs conv to floats
		vals = []
		for val in line:
			val = float( val )
			vals.append( float( val ) )
		aa2scores[ aa ] = vals
	return aa2scores


def load_mat( filename ):
	f = open( filename, 'r' )
	file = f.readlines()
	#WARNING hardcoded, line 0 = comments, line 1 = col labels, symmetric
	col_aas = file[ 1 ].rstrip().split()
	#dict of aa letter -> substitution score vector
	aa2vec = {}
	for il in range( 2, len( file ) ):
		line = file[ il ]
		toks = line.rstrip().split()
		row_aa = toks[ 0 ]
		#is this row label in our allowed aa_types?
		assert( row_aa in aa_types ), 'found aa ' + row_aa + ' not in allowed aa_types!'
		aa2vec[ row_aa ] = []
		for itok in range( 1, len( toks ) ):
			#what is the colum label for this value?
			col_aa = col_aas[ itok - 1 ]
			#is this column label in our allowed aa_types?
			#GETTING RID OF SYMMETRY REQUIREMENT
#			if col_aa not in aa_types: continue
			val = float( toks[ itok ] )
			aa2vec[ row_aa ].append( val )
	f.close()
	return aa2vec

## xform ic50 values into nonbinder = [0,1] = strong binder
def ic50_log_xform( ic50 ):
	score = 1 - math.log( ic50 ) / math.log( 50000 )
	return score

#returns a list-list, [ seqpos ][ feat_vec ]
def seq2features( seq, aa2vec ):
	features = []
	for aa in seq:
#		assert( aa2vec.has_key( aa ) ),\
#			'no feature_matrix entry for ' + aa + ' in sequence ' + seq

		## BUG:FIXED##
		# everything in pythnon is a pointer, we need to deep copy the list, not just make a pointer to it!
		#feat_vec = aa2vec[ aa2vec[ aa ] ]
		## BUG:FIXED##
		try:
			features.append( aa2vec[ aa ][ : ] )
		except:
			features.append( aa2vec[ 'X' ][ : ] )
	return features

#WARNING HARDCODED: flanking residues are first and last 3
def avg_pfr_features( features ):
	nterm_avg = []
	cterm_avg = []
	#over seqpos feature length, weighted avg of terminal features
	#avging goes like (/)---------(\) so pfr closer to core count more			
	for ival in range( len( features[ 0 ] ) ):
		nterm_avg.append( (1./6.) * features[ 0 ][ ival ] + (2./6.) * features[ 1 ][ ival ] + (3./6.) * features[ 2 ][ ival ] )
		cterm_avg.append( (1./6.) * features[ -1 ][ ival ] + (2./6.) * features[ -2 ][ ival ] + (3./6.) * features[ -3 ][ ival ] )
	new_features = []
	new_features.append( nterm_avg )
	for aavec in features[ 3:-3 ]:
		new_features.append( aavec )
	new_features.append( cterm_avg )
	return new_features

#append feature vector for length of termini feature sets
#value is fraction of max term length shifted and scaled
def add_missing_term_features( seq, seq_features ):
	len_term = ( len( seq ) - 9 ) / 2
	n_miss = 2 * ( float( seq[ :len_term ].count( '-' ) ) / float( len_term ) ) - 1
	c_miss = 2 * ( float( seq[ -len_term: ].count( '-' ) ) / float( len_term ) ) - 1
	seq_features.append( [ n_miss, c_miss ] )

#add pssm scores for each position as last feature set
def add_pssm_features( seq, seq_features, pssm_aa2scores ):
	
	pssm_features = []
	#get pssm offset, maybe pssm is 9mer but is in middle
	len_pssm = len( pssm_aa2scores.values()[ 0 ] )
	offset = int( ( len( seq ) - len_pssm ) / 2 )
	for iseq in range( offset, offset + len_pssm ):
		if offset < 0:
			print 'ERROR: sequence is shorter than pssm!'
			sys.exit()
		aa = seq[ iseq ]
		#default to min score if aa not found in pssm
		try:
			score = pssm_aa2scores[ aa ][ iseq - offset ]
		except:
			score = float( -1. )
		pssm_features.append( score )
#	print seq, pssm_features
	seq_features.append( pssm_features )


#parses iedb data into libsvm format, transforms sequence into feature vector, each aa is a blosum row
sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	icol_seq = int( sys.argv.pop( 0 ) ) - 1
	icol_val = sys.argv.pop( 0 )
except:
	print "args:\tseq_data\tseq_col\tval_col(-)\t<aa_feature_matrix(-)>\tavg_pfr(f|t)\tmissing_term(f|t)\t<pssm(-)>"
	sys.exit()

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

#if bogus val colum, default to 0 valuer
try:
	icol_val = int( icol_val ) - 1
except:
	icol_val = None

try:
	aa2vec = load_mat( sys.argv.pop( 0 ) )
except:
	aa2vec = load_mat( '/work/chrisk/Rosetta/main/database/sequence/substitution_matrix/BLOSUM62.prob.rescale' )
try:
	avg_pfr = sys.argv.pop( 0 )
	if avg_pfr.lower()[ 0 ] == 'f': avg_pfr = False
except:
	avg_pfr = False
try:
	miss_term = sys.argv.pop( 0 )
	if miss_term.lower()[ 0 ] == 'f': miss_term = False
except:
	miss_term = False
try:
	pssm = open( sys.argv.pop( 0 ) ).readlines()
except:
	pssm = False

pssm_aa2scores = []
if pssm: pssm_aa2scores = load_pssm( pssm )

for line in file:
	toks = line.rstrip().split()
	#linearize ic50 into bind score
	if icol_val is None:
		bind_score = 0
	#if listed binding value is 1 or 0 (true/false for classification), just use 1 or 0
	#WARNING THIS IS SUPER HACKY AND BOUND TO FUCKUP EVENTUALLY
	elif toks[ icol_val ] == '1' or toks[ icol_val ] == '0':
		bind_score = int( toks[ icol_val ] )
	#else transform to [0,1]
	#WARNING will reset to 0.0 or 1.0 if exceeds allowed [0,1] domain!
	else:
		ic50 = float( toks[ icol_val ] )
		bind_score = ic50_log_xform( ic50 )
		if bind_score > float( 1.0 ): bind_score = 1.0
		elif bind_score < float( 0.0 ): bind_score = 0.0
	seq = toks[ icol_seq ]
	sys.stdout.write( str( bind_score ) + ' ' )
	#get sequence features [seqpos][aaidx] from feature matrix
	seq_features = seq2features( seq, aa2vec )
	if avg_pfr: seq_features = avg_pfr_features( seq_features )
	if miss_term: add_missing_term_features( seq, seq_features )
	if pssm: add_pssm_features( seq, seq_features, pssm_aa2scores )
	ifeat = 1 #feature index
	for iseq, aa_features in enumerate( seq_features ):
		for val in aa_features:
			sys.stdout.write( str( ifeat ) + ':' + ( '%.3f' % val ) + ' ' )
			ifeat += 1
	sys.stdout.write( '\n' )
