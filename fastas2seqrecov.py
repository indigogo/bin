#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tfasta\tfasta2"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
filename2 = sys.argv.pop( 0 )

file = open( filename, 'r' ).readlines()
seq = ''
for line in file:
	if line[ 0 ] == '>': continue
	seq += line.strip()

file2 = open( filename2, 'r' ).readlines()
seq2 = ''
for line in file2:
	if line[ 0 ] == '>': continue
	seq2 += line.strip()

if len( seq ) != len( seq2 ):
	print "ERROR: diff length fasta seqs!"
	sys.exit()

n_diff = 0
for i in range( len( seq ) ):
	if seq[ i ] != seq2[ i ]: n_diff += 1.0
print '%.3f' % ( 1.0 - n_diff / len( seq ) )
	
