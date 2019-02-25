#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tfasta\tnmer_length"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
n = int( sys.argv.pop( 0 ) )

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
		for iseq in range( len( seq ) - n + 1 ):
			nmer = seq[ iseq:(iseq + n) ]
			if not counts.has_key( nmer ): counts[ nmer ] = 1
			else: counts[ nmer ] += 1
for key, val in counts.iteritems():
	print key, val
