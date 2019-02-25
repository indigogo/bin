#!/usr/bin/python

import sys
import os
import math

def load_fasta_seq( file ):
	seq = ''
	for line in file:
		if line[ 0 ] == '>': continue
		seq += line.strip()
	return seq


#parses fasta into Nmers, libsvm format, transforms sequence into feature vector, each aa is a blosum row
sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	seqlength = int( sys.argv.pop( 0 ) )
except:
	print "args:\tfasta\tseqlength"
	sys.exit()

if filename == '-':
	file = sys.stdin.readlines()
else:
	file = open( filename, 'r' ).readlines()

seq = load_fasta_seq( file )
for iseq in range( len( seq ) - ( seqlength - 1 ) ):
	subseq = seq[ iseq:iseq+seqlength ]
	sys.stdout.write( subseq + '\n' )
