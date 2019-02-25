#!/usr/bin/python

import sys
import os
import re

if( len( sys.argv ) < 2 ):
	print "args:\tfasta\tpdb\tseqfile"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
subseqs = open( sys.argv.pop( 0 ) ).readlines()

file = open( filename, 'r' ).readlines()
il = 0
counts = {}
epicounts = {}
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
			#skip comments or fasta nametags
			if subseq[ 0 ] == '#' or subseq[ 0 ] == '>': continue
			count = seq.count( subseq )
			if count:
				#finditer returns an iterable MatchObject
				#match.start() is the index of the first character of the matched substring
				iseqs = [ match.start() for match in re.finditer( re.escape( subseq ), seq ) ]
				for iseq in iseqs:
					if not epicounts.has_key( iseq ): epicounts[ iseq ] = 1
					else: epicounts[ iseq ] += 1
				#if not counts.has_key( subseq ): counts[ subseq ] = count
				#else: counts[ subseq ] += count

#now match ep res indices to pdb indices, need nterm offset
#this will break only if pdb is missing nterm epitopes
pdb = open( pdbname, 'r' ).readlines()
ires1_pdb = None
pdb_res = []
chain = None
for il,line in enumerate( pdb ):
  if not line.startswith( 'ATOM' ): continue
  if chain is None: chain = line[ 21 ]
  elif line[ 21 ] != chain: continue
  #store res index of existing residue (in case of missing res)
  ires_pdb = int( line[ 22:26 ].strip() )
  if ires_pdb not in pdb_res: pdb_res.append( ires_pdb )
  if ires1_pdb is None:
    ires1_pdb = ires_pdb

pdb = open( pdbname, 'r' ).readlines()
for ires in sorted( epicounts.iterkeys() ):
  count = epicounts[ ires ]
  ires_ep_pdb = ires + ires1_pdb
  if ires_ep_pdb not in pdb_res: continue
  print str( ires_ep_pdb ), chain, str( count )

#for key, val in counts.iteritems():
#	print key, val
