#!/usr/bin/python

# this scores all seqs in a fasta by sliding an input pssm over each sequence

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tfasta\tpssm\t<verbose>"
	sys.exit()
sys.argv.pop( 0 )
fastaname = sys.argv.pop( 0 )
pssmname = sys.argv.pop( 0 )
try:
	verbose = sys.argv.pop( 0 )
except:
	verbose = False

pssm = open( pssmname, 'r' ).readlines()
pssm_length = None
aa2scores = {}
aas = []
#load the pssm data
for line in pssm:
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
		vals.append( val )
	aa2scores[ aa ] = vals

#read seqs
fasta = open( fastaname, 'r' ).readlines()
seq = ''
seqs = []
for i, line in enumerate( fasta ):
	line = line.strip()
	if line[ 0 ] == '#': continue #skip comments
	if line[ 0 ] == '>':
		#if seq has a cached sequence, store it in seqs and clear
		if len( seq ) > 0:
			seqs.append( seq )
		seq = ''
		continue
	seq += line 
#and one last time for EOF
if len( seq ) > 0:
	seqs.append( seq )
	
#score seqs
for seq in seqs:
	score = 0.
	for iseq1 in range( len( seq ) - pssm_length + 1 ):
		subseq = ''
		for ipssm in range( pssm_length ):
			iseq = iseq1 + ipssm
			aa = seq[ iseq ]
			subseq += aa
			try:
				score += aa2scores[ aa ][ ipssm ]
			except:
				score += 0
		if verbose:
			print subseq, str( score )
			score = 0
	if not verbose: print seq, str( score )

