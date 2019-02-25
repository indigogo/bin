#!/usr/bin/python

import sys
import os

aa3_to_aa1 = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
              'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
              'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
              'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
              'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

sys.argv.pop( 0 )
try:
	tablename = sys.argv.pop( 0 )
except:
	print "args:\tGreedyOptTable\t<transform(lin,exp,norm,colnorm)>\t<scale(1)>"
	sys.exit()
try:
	transform = sys.argv.pop( 0 )
#	assert( transform == 'lin' or transform == 'exp' ), 'transform options are lin or exp'
except:
	transform = 'lin'
try:
	scale = float( sys.argv.pop( 0 ) )
except:
	scale = 1.0

table = open( tablename, 'r' ).readlines()
seqpos_aa3_scores = {}
aa3_seqpos_scores = {}
seqpos_max_vals = {}
seqpos_min_vals = {}
for line in table:
	line = line.rstrip().split()
	if len( line ) < 2: continue
	seqpos = int( line[ 0 ] )
	#parse each aa3,val pair
	aa3_scores = {}
	seqpos_max_val = None
	seqpos_min_val = None
	for itok in range( 3, len( line ) ):
		aa3 = line[ itok ].split( ':' )[ 0 ].rstrip( '*' )
		val = float( line[ itok ].split( ':' )[ 1 ] )
		if not aa3_seqpos_scores.has_key( aa3 ):
			aa3_seqpos_scores[ aa3 ] = {}
		aa3_seqpos_scores[ aa3 ][ seqpos ] = val
		if not seqpos_aa3_scores.has_key( seqpos ):
			seqpos_aa3_scores[ seqpos ] = {}
		seqpos_aa3_scores[ seqpos ][ aa3 ] = val
		if seqpos_max_val == None:
			seqpos_max_val = val
			seqpos_min_val = val
		elif val > seqpos_max_val:
			seqpos_max_val = val
		elif val < seqpos_min_val:
			seqpos_min_val = val
	seqpos_max_vals[ seqpos ] = seqpos_max_val
	seqpos_min_vals[ seqpos ] = seqpos_min_val
max_val = sorted( seqpos_max_vals.values() )[ -1 ]
min_val = sorted( seqpos_min_vals.values() )[ 1 ]

#sort by aa3
for aa3 in sorted( aa3_seqpos_scores.iterkeys() ):
	sys.stdout.write( aa3_to_aa1[ aa3 ] + '\t' )
	for seqpos in sorted( aa3_seqpos_scores[ aa3 ].iterkeys() ):
		#just flip sign?
		if transform == 'lin':
			val = -1 * ( aa3_seqpos_scores[ aa3 ][ seqpos ] )
		#or shift pssm minimum to zero?
#		val = -1 * ( aa3_seqpos_scores[ aa3 ][ seqpos ] - max_val )
		#or shift pssm minimum to zero by seqpos?
#		val = -1 * ( aa3_seqpos_scores[ aa3 ][ seqpos ] - seqpos_max_vals[ seqpos ] )
		#or shift and scale pssm to [0,1] 
		elif transform == 'norm':
			val = ( aa3_seqpos_scores[ aa3 ][ seqpos ] - max_val ) / ( min_val - max_val )
		#or shift and scale pssm to [0,1] by seqpos?
		elif transform == 'colnorm':
			val = ( aa3_seqpos_scores[ aa3 ][ seqpos ] - seqpos_max_vals[ seqpos ] ) / ( seqpos_min_vals[ seqpos ] - seqpos_max_vals[ seqpos ] )

		val = val * scale
		val = '%.3f' % val
		sys.stdout.write( val + '\t' )
	sys.stdout.write( '\n' )
