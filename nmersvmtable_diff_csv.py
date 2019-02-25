#!/usr/bin/python

import sys
import os
from math import exp, log

def bind2score( bind ):
	return ( 1. - log( bind ) / log( 50000. ) )
def score2bind( score ):
	return ( exp( ( 1 - score ) * log( 50000 ) ) )

sys.argv.pop( 0 )
try:
	tablename = sys.argv.pop( 0 )
except:
	print "args:\tsvm_table1\tcutoff( 0.0 or 50000nm )\t<pdb_chain>\t<verbose(f|t)>"
	sys.exit()
try:
  epcut = sys.argv.pop( 0 ) 
  #xform epcut from nM input to score?
  if epcut[ -2: ].lower() == 'nm':
    epcut = bind2score( float( epcut[ :-2 ] ) )
  else:
    epcut = float( epcut )
except:
  epcut = 0.0
try:
	chain = sys.argv.pop( 0 ).upper()
except:
	chain = False
try:
	verbose = sys.argv.pop( 0 )
	if verbose[ 0 ].lower() == 't': verbose = True
	else: verbose = False
except:
	verbose = False


table = open( tablename, 'r' ).readlines()

#find all table nmers indexed by nettable output
for line in table:
	toks = line.rstrip().split()
	nmer_score = float( toks[ -1 ].split( ':' )[ -1 ] )
	seq = toks[ 2 ]
	#skip if wrong chain, same seq or either below ep score cutoff
	if chain and toks[ 1 ] != chain: continue
#	if seq == seq2: continue
	if nmer_score < epcut : continue
	print toks[ 0 ], toks[ 1 ], toks[ 2 ], nmer_score,
	#print diff of all, or just AVG?
	if verbose: itok_first = 3
	else: itok_first = len( toks ) - 1
	for itok in range( itok_first, len( toks ) ):
		svm_idx = toks[ itok ].split( ':' )[ 0 ]
		nmer_score = float( toks[ itok ].split( ':' )[ -1 ] )
		nmer_bind = score2bind( nmer_score )
#		print svm_idx + ':' + '%.3f' % ( nmer_score2 - nmer_score ) + '|' + '%.1f' % nmer_bind + '->' + '%.1f' % nmer_bind2,
		print  '%.1f' % nmer_bind ,
	print

