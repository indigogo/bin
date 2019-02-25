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
	tablename2 = sys.argv.pop( 0 )
except:
	print "args:\tsvm_table1\tsvm_table2\tcutoff( 0.0 or 50000nm )\t<pdb_chain>\t<verbose(f|t)>\t<print_by_allele(f|t)>"
	sys.exit()
try:
  epcut = sys.argv.pop( 0 ) 
  #xform epcut from nM input to score?
  if epcut[ -2: ].lower() == 'nm':
    epcut = bind2score( float( epcut[ :-2 ] ) )
  else:
    epcut = float( epcut )
except:
  epcut = float( -9999 )
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
try:
	print_by_allele = sys.argv.pop( 0 )
	if print_by_allele[ 0 ].lower() == 't': print_by_allele = True
	else: print_by_allele = False
except:
	print_by_allele = False

showdiff = True
if tablename2 == '-':
	tablename2 = tablename
	showdiff = False

table = open( tablename, 'r' ).readlines()
table2 = open( tablename2, 'r' ).readlines()
assert( len( table ) == len( table2 ) ), "Tables are of different size! We're doing line-wise comparison."

#find all table nmers indexed by nettable output
for line ,line2 in zip( table, table2 ):
	toks = line.rstrip().split()
	nmer_score = float( toks[ -1 ].split( ':' )[ -1 ] )
	seq = toks[ 2 ]
	toks2 = line2.rstrip().split()
	nmer_score2 = float( toks2[ -1 ].split( ':' )[ -1 ] )
	seq2 = toks2[ 2 ]
	#skip if wrong chain, same seq or either below ep score cutoff
	if chain and toks[ 1 ] != chain: continue
#	if seq == seq2: continue
	#skip if 2 diff files and info is same
	if tablename2 != tablename and nmer_score == nmer_score2: continue
	#print diff of all, or just AVG?
	if verbose: itok_first = 3
	else: itok_first = len( toks ) - 1
	#print one line for each allele and leave off avg?
	if print_by_allele: 
		for itok in range( itok_first, len( toks ) - 1 ):
			svm_idx = toks[ itok ].split( ':' )[ 0 ]
			nmer_score = float( toks[ itok ].split( ':' )[ -1 ] )
			nmer_score2 = float( toks2[ itok ].split( ':' )[ -1 ] )
			nmer_bind = score2bind( nmer_score )
			nmer_bind2 = score2bind( nmer_score2 )
			if ( nmer_score <= epcut and nmer_score2 <= epcut ): continue
			if showdiff:
				print toks[ 0 ], toks[ 1 ], toks[ 2 ] + '-' + toks2[ 2 ],
				print svm_idx + ':' + '%.3f' % ( nmer_score2 - nmer_score ) + '|' + '%.1f' % nmer_bind + '->' + '%.1f' % nmer_bind2
			else:
				print toks[ 0 ], toks[ 1 ], toks[ 2 ],
				print svm_idx + ':' + '%.3f' % ( nmer_score ) + '|' + '%.1f' % nmer_bind 
	else: 
		if ( nmer_score <= epcut and nmer_score2 <= epcut ): continue
		if showdiff:
			print toks[ 0 ], toks[ 1 ], toks[ 2 ] + '-' + toks2[ 2 ],
		else:
			print toks[ 0 ], toks[ 1 ], toks[ 2 ],
		for itok in range( itok_first, len( toks ) ):
			svm_idx = toks[ itok ].split( ':' )[ 0 ]
			nmer_score = float( toks[ itok ].split( ':' )[ -1 ] )
			nmer_score2 = float( toks2[ itok ].split( ':' )[ -1 ] )
			nmer_bind = score2bind( nmer_score )
			nmer_bind2 = score2bind( nmer_score2 )
			if showdiff:
				print svm_idx + ':' + '%.3f' % ( nmer_score2 - nmer_score ) + '|' + '%.1f' % nmer_bind + '->' + '%.1f' % nmer_bind2,
			else:
				print svm_idx + ':' + '%.3f' % ( nmer_score ) + '|' + '%.1f' % nmer_bind,
		print

