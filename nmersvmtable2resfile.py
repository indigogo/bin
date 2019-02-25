#!/usr/bin/python

import sys
import os
from math import exp, log

sys.argv.pop( 0 )
try:
	tablename = sys.argv.pop( 0 )
except:
	print "args:\tsvm_table\tcutoff( 0.425 or 500nm )\t<pdb_chain>\t<term_len(0)>"
	sys.exit()
try:
	epcut = sys.argv.pop( 0 ) 
  #xform epcut from nM input to score?
	if epcut[ -2: ].lower() == 'nm':
		epcut = 1. - log( float( epcut[ :-2 ] ) ) / log( 50000. )
	else:
		epcut = float( epcut )
except:
	epcut = 0.425625189
try:
	chain = sys.argv.pop( 0 ).upper()
except:
	chain = False
try:
	term_len = int( sys.argv.pop( 0 ) )
except:
	term_len = 0

table = open( tablename, 'r' ).readlines()

#find all table nmers indexed by nettable output
epres = []
for il,line in enumerate( table ):
	toks = line.rstrip().split()
	nmer_score = float( toks[ -1 ].split( ':' )[ -1 ] )
	if nmer_score < epcut: continue
	nmer_seq = toks[ 2 ]
	#skip chain?
	if chain and toks[ 1 ] != chain: continue
	for inmer in range( il - term_len, il + len( nmer_seq ) + term_len ):
		try:
			toks = table[ inmer ].rstrip().split()
			reschain = toks[ 0 ] + ' ' + toks[ 1 ]
			if reschain not in epres: epres.append( reschain )
		except:
			continue
print 'NATAA\nstart'
for reschain in epres:
	print reschain, 'ALLAAxc'

