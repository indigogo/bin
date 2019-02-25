#!/usr/bin/python

import sys
import os

aas = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', \
 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

sys.argv.pop( 0 )
try:
	fastaname = sys.argv.pop( 0 )
except:
	print "args:\tfastaname"
	sys.exit()

fasta = open( fastaname, 'r' ).readlines()
seq = ''
for line in fasta:
	if line[ 0 ] == '>': continue
	seq += line.strip()
outname = '.'.join( fastaname.split( '.' )[ :-1 ] ) 

out = open( outname + '.ptmuts.fasta', 'w' )
out.write( '>input\n' )
out.write( seq + '\n' )
for iseq in range( len( seq ) ):
	for aa in aas:
		#dont repeat the input!
		if seq[ iseq ] == aa: continue
		mutseq = seq
		mutseq = seq[ 0:iseq ] + aa + seq[ ( iseq + 1 ): ]
		out.write( '>' + str( iseq ) + aa + '\n' )
		out.write( mutseq + '\n' )
out.close
