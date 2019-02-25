#!/usr/bin/python

import sys
import os

def load_fasta_seqs( file ):
	seq = ''
	seqs = []
	tags = []
	read_first = False
	for il, line in enumerate( file ):
		if line[ 0 ] == '>':
			tags.append( line.rstrip() )
			if not read_first:
				read_first = True
			else:
				seqs.append( seq )
				seq = ''
			continue
		seq += line.strip()
	seqs.append( seq ) # the last seq
	return seqs, tags

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	file2name = sys.argv.pop( 0 )
except:
	print "args:\tfasta1\tfasta2"
	sys.exit()

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()
file2 = open( file2name, 'r' ).readlines()

[ seqs, tags ] = load_fasta_seqs( file )
[ seqs2, tags2 ] = load_fasta_seqs( file2 )

for iseq in range( len( seqs ) ):
	seq = seqs[ iseq ]
	for iseq2 in range( len( seqs2 ) ):
		print tags[ iseq ], tags2[ iseq2 ]
		seq2 = seqs2[ iseq2 ]
		for i,aa in enumerate( zip( seq, seq2 ) ):
			if aa[ 0 ] == aa[ 1 ]: continue
			print i+1, aa[ 0 ], aa[ 1 ]
	


