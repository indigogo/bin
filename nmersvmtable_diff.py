#!/usr/bin/python

import sys
import os
from math import exp, log
import re

def bind2score( bind ):
	return ( 1. - log( bind ) / log( 50000. ) )
def score2bind( score ):
	return ( exp( ( 1 - score ) * log( 50000 ) ) )

sys.argv.pop( 0 )
try:
	tablename = sys.argv.pop( 0 )
	tablename2 = sys.argv.pop( 0 )
except:
	print "args:\tsvm_table1\tsvm_table2\tcutoff( 0.0 or 50000nm )\t<pdb_chain(-)>\t<verbose(f|t)>"
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
	if chain == '-': chain = False
except:
	chain = False
try:
	verbose = sys.argv.pop( 0 )
	if verbose[ 0 ].lower() == 't': verbose = True
	else: verbose = False
except:
	verbose = False

if tablename2 == '-': tablename2 = tablename

table = open( tablename, 'r' ).readlines()
table2 = open( tablename2, 'r' ).readlines()
assert( len( table ) == len( table2 ) ), "Tables are of different size! We're doing line-wise comparison."
#use regexp to check if line has an ep seq
is_seq_rxp = re.compile( '[A-Z]+' )
#find all table nmers indexed by nettable output
for line ,line2 in zip( table, table2 ):
	toks = line.rstrip().split()
	seq = toks[ 2 ]
	toks2 = line2.rstrip().split()
	seq2 = toks2[ 2 ]
	#skip if wrong chain, same seq or either below ep score cutoff
	if chain and toks[ 1 ] != chain: continue
	if seq == seq2: continue
	#print diff of all, or just AVG?
	if verbose: itok_first = 3
	else: itok_first = len( toks ) - 1
	for itok in range( itok_first, len( toks ) ):
		#if has no ep seq, is bogus tail line where score fell off end of chain
		#TODO fix this in rosetta so not printed?
		if not is_seq_rxp.match( toks[ 2 ] ): continue
		nmer_score = float( toks[ itok ].split( ':' )[ -1 ] )
		nmer_score2 = float( toks2[ itok ].split( ':' )[ -1 ] )
		if nmer_score < epcut and nmer_score2 < epcut: continue
		#skip if 2 diff files and info is same
		if tablename2 != tablename and nmer_score == nmer_score2: continue
		print toks[ 0 ], toks[ 1 ], toks[ 2 ] + ' -> ' + toks2[ 2 ],
		svm_idx = toks[ itok ].split( ':' )[ 0 ]
		nmer_score = float( toks[ itok ].split( ':' )[ -1 ] )
		nmer_score2 = float( toks2[ itok ].split( ':' )[ -1 ] )
		nmer_bind = score2bind( nmer_score )
		nmer_bind2 = score2bind( nmer_score2 )
		print 'svm' + svm_idx + ' ' '%.3f' % ( nmer_score ) + ' -> ' + '%.3f' % ( nmer_score2 ) + ' | ' + '%.1f' % nmer_bind + ' -> ' + '%.1f' % nmer_bind2

