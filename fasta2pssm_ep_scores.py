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

def load_seqs( file ):
	seq = ''
	seqs = []
	for il, line in enumerate( file ):
		seqs.append( line.strip() ) 
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

#input: fasta, allele_pssm name
sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	allele_pssm = sys.argv.pop( 0 )
except:
	print "args:\tfastaname\tpssm\t<peptide_mode(f|t)>"
	sys.exit()
try:
	peptide_mode = sys.argv.pop( 0 )
	if peptide_mode.lower()[ 0 ] == 'f': peptide_mode = False
except:
	peptide_mode = False

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()


#was this a stupid fasta file, or a sensible 1 sequence per line file?
if filename.split( '/' )[ -1 ].split( '.' )[ -1 ] == 'fasta': fasta_seqs = load_fasta_seqs( file )
else: fasta_seqs = load_seqs( file )
#foreach fasta entry
tmpname = '.tmp.' + filename + '.' + allele_pssm.replace( '/', '.' )
for fasta_seq in fasta_seqs:
	fasta_seq = clean_seq( fasta_seq )
	if len( fasta_seq ) < 9: continue
	#print fasta seq
	out = open( tmpname, 'w' )
	out.write( '>tmp\n' + fasta_seq )
	out.close()
	os.system( 'pssm_score_fasta.py ' + tmpname + ' ' + allele_pssm + ' verbose > ' + tmpname+'.predict' )
	#get index of highest score
	pred_in = open( tmpname+'.predict', 'r' ).readlines()

	pred_scores = []
	nmer_seqs = []
	for line in pred_in:
		pred_scores.append( float( line.strip().split()[ 1 ] ) )
		nmer_seqs.append( line.strip().split()[ 0 ] )
	assert( len( nmer_seqs ) == len( pred_scores ) ), 'number nmer_seqs not equal to number predicted scores in ' + tmpname+'.predict'
	if not peptide_mode:
		for pep_score in zip( nmer_seqs, pred_scores ):
			print pep_score[ 0 ], pep_score[ 1 ]
	else:
		max_score = max( pred_scores )
		idx_max_score = pred_scores.index( max( pred_scores ) )
		#use index to find best scoring 15mer sequence
		print nmer_seqs[ idx_max_score ], max_score
