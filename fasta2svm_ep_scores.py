#!/usr/bin/python

import sys
import os

def load_fasta_seqs( file ):
	seq = ''
	seqs = []
	read_first = False
	for il, line in enumerate( file ):
		if line[ 0 ] == '>':
			if not read_first:
				read_first = True
			else:
				seqs.append( seq )
				seq = ''
			continue
		seq += line.strip()
	seqs.append( seq ) # the last seq
	return seqs

def load_seqs( file, seqcol ):
	seq = ''
	seqs = []
	for il, line in enumerate( file ):
		seqs.append( line.strip().split()[ seqcol ] ) 
	return seqs

def seq2nmer_seqs( seq, n_core, n_term ):
#	assert( len( seq ) >= n_core ), 'sequence %s is too short!' % seq
	if len( seq ) < n_core: return []
	nmer_seqs = []
	for iseq in range( len( seq ) - n_core + 1 ):
		nmer_seq = seq[ iseq:(iseq + n_core) ]
		for iterm in range( 1, n_term+1 ):
			if iseq - iterm >= 0:
				nmer_seq = seq[ iseq - iterm ] + nmer_seq
			else:
				nmer_seq = 'X' + nmer_seq
			if iseq + n_core + iterm - 1 <= len( seq ) - 1:
				nmer_seq = nmer_seq + seq[ iseq + n_core + iterm - 1 ]
			else:
				nmer_seq = nmer_seq + 'X'
		nmer_seqs.append( nmer_seq )
	return nmer_seqs

def clean_seq( seq ):
	aas = 'ACDEFGHIKLMNPQRSTVWYX'
	for iseq in range( len( seq ) ):
		if seq[ iseq ] not in aas: seq = seq.replace( seq[ iseq ], 'X' )
	return seq

#input: fasta, allele name
sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	model_fname = sys.argv.pop( 0 )
	pssm_fname = sys.argv.pop( 0 )
except:
	print "args:\tfastaname\tmodel_fname\tpssm_fname\t<peptide_mode(f|t)>\t<seqcol>"
	sys.exit()
try:
	peptide_mode = sys.argv.pop( 0 )
	if peptide_mode.lower()[ 0 ] == 'f': peptide_mode = False
except:
	peptide_mode = False
try:
	seqcol = int( sys.argv.pop( 0 ) ) - 1
except:
	seqcol = 0

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

#was this a stupid fasta file, or a sensible 1 sequence per line file?
if filename.split( '/' )[ -1 ].split( '.' )[ -1 ] == 'fasta': fasta_seqs = load_fasta_seqs( file )
else: fasta_seqs = load_seqs( file, seqcol )
#foreach fasta entry
tmpname = '.tmp.' + filename + '.' + model_fname.split( '/' )[ -1 ]
for fasta_seq in fasta_seqs:
	fasta_seq = clean_seq( fasta_seq )
	#print each 9mer frame w/ 3mer termini (incl Xs) = 15mer to file and store in list
	nmer_seqs = seq2nmer_seqs( fasta_seq, 9, 3 )
	if len( nmer_seqs ) == 0: continue
	out = open( tmpname, 'w' )
	for seq in nmer_seqs: out.write( seq + '\n' )
	out.close()
	#run data2libsvm.py on 15mer sequences
	os.system( 'data2libsvm.py '+tmpname+' 1 - - f t f ' + pssm_fname + ' >& '+tmpname+'.libsvm.dat' )
	#run svm-predict on 15mer libsvm data
	os.system( 'svm-predict ' + tmpname + '.libsvm.dat ' + model_fname + ' ' + tmpname+'.predict >& '+tmpname+'.out' )
	#get index of highest score
	pred_in = open( tmpname+'.predict', 'r' ).readlines()
	pred_scores = []
	for line in pred_in: pred_scores.append( float( line.strip() ) )
	assert( len( nmer_seqs ) == len( pred_scores ) ), 'number nmer_seqs not equal to number predicted scores in ' + tmpname+'.predict'
	if not peptide_mode:
		for pep_score in zip( nmer_seqs, pred_scores ):
			print pep_score[ 0 ], pep_score[ 1 ]
	else:
		max_score = max( pred_scores )
		idx_max_score = pred_scores.index( max( pred_scores ) )
		#use index to find best scoring 15mer sequence
		print nmer_seqs[ idx_max_score ], max_score
