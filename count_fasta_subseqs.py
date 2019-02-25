#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tfasta\tseqfile"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
subseqs = open( sys.argv.pop( 0 ) ).readlines()

file = open( filename, 'r' ).readlines()
il = 0
counts = {}
while il <= len( file ) - 1:
	#if new sequence
	if file[ il ][ 0 ] == '>':
		#init seq, goto next line
		seq = ''
		il +=1
		#accum seq until next entry or EOF
		while il <= len( file ) - 1 and file[ il ][ 0 ] != '>':
			seq += file[ il ].strip()
			il += 1
		#incr dict val for each nmer
		for subseq in subseqs:
			subseq = subseq.split()[ 0 ].rstrip()
			count = seq.count( subseq )
			if count:
				if not counts.has_key( subseq ): counts[ subseq ] = count
				else: counts[ subseq ] += count
for key, val in counts.iteritems():
	print key, val
