#!/usr/bin/python

# this calcs enrichment (log odds) b/t 2 pssms

import sys
import os
import math

def load_pssm( pssmfile ):
	pssm_length = None
	aa2scores = {}
	aas = []
	for line in pssmfile:
		line = line.split()
		if line[ 0 ][ 0 ] == '#': continue #skip comments
		aa = line.pop( 0 ) #rest of line is vals
		aas.append( aa )
		#init pssm_length, else die if inconsistent
		if pssm_length is None: pssm_length  = len( line )
		elif pssm_length != len( line ):
			print "inconsistent N entries at aa " + aa
			sys.exit()
		#store vals, needs conv to floats
		vals = []
		for val in line:
			val = float( val )
			vals.append( val )
		aa2scores[ aa ] = vals
	return aa2scores

def calc_ratio_pssm( pssm, pssm_bg, min_val ):
	pssm_ratio = pssm
	for aa in pssm.iterkeys():
		assert pssm_bg.has_key( aa ), 'ERROR: aa ' + aa + ' not found in background pssm!'
		for iseq in range( len( pssm[ aa ] ) ):
			assert iseq <= len( pssm_bg[ aa ] ), 'ERROR: background pssm has wrong number columns for aa ' + aa
			if pssm[ aa ][ iseq ] == 0.0: pssm[ aa ][ iseq ] = min_val
			if pssm_bg[ aa ][ iseq ] == 0.0: pssm_bg[ aa ][ iseq ] = min_val
			pssm_ratio[ aa ][ iseq ] = ( pssm[ aa ][ iseq ] / pssm_bg[ aa ][ iseq ] )
	return pssm_ratio

# How to deal with zero entries in log odds?
# set all zeros to minimum value == 0.001
def calc_log_odds_pssm( pssm, pssm_bg, min_val ):
	#init pssm
	pssm_log = pssm
	#init w/ input so is same size, n elements
	pssm_ratio = calc_ratio_pssm( pssm, pssm_bg, min_val )
	for aa in pssm.iterkeys():
		assert pssm_bg.has_key( aa ), 'ERROR: aa ' + aa + ' not found in background pssm!'
		for iseq in range( len( pssm[ aa ] ) ):
			assert iseq <= len( pssm_bg[ aa ] ), 'ERROR: background pssm has wrong number columns for aa ' + aa
			if pssm_ratio[ aa ][ iseq ] == 0.0: pssm_ratio[ aa ][ iseq ] = min_val
			pssm_log[ aa ][ iseq ] = math.log( pssm_ratio[ aa ][ iseq ] )
	return pssm_log

# rescale values linearly to [rsc_min,rsc_max]
# rescales by entire matrix min,max, NOT by column
def rescale_pssm( pssm, rsc_min, rsc_max ):
	#get current min,max
	min = None
	max = None
	for aa in pssm.iterkeys():
		for iseq in range( len( pssm[ aa ] ) ):
			if min is None or pssm[ aa ][ iseq ] < min: min = pssm[ aa ][ iseq ]
			if max is None or pssm[ aa ][ iseq ] > max: max = pssm[ aa ][ iseq ]
	#rescale values in-place
	for aa in pssm.iterkeys():
		for iseq in range( len( pssm[ aa ] ) ):
			#rescale to [0,1]
			pssm[ aa ][ iseq ] = ( pssm[ aa ][ iseq ] - min ) / ( max - min )
			#then to rsc_min,rsc_max
			pssm[ aa ][ iseq ] = ( rsc_max - rsc_min ) * pssm[ aa ][ iseq ] + rsc_min

def print_pssm( pssm ):
	for aa in sorted( pssm.iterkeys() ):
		sys.stdout.write( aa )
		for iseq in range( len( pssm[ aa ] ) ):
			sys.stdout.write( '\t' + '%.3f' % pssm[ aa ][ iseq ] )
		sys.stdout.write( '\n' )

if( len( sys.argv ) < 2 ):
	print "args:\tpssm\tpssm_bg\t<type(logodds||ratio)>\t<pseudofreq(0.001)>\t<rescale[-1,1](f|t)>"
	sys.exit()
sys.argv.pop( 0 )
pssmname = sys.argv.pop( 0 )
pssm_bgname = sys.argv.pop( 0 )
try:
	type = sys.argv.pop( 0 )
except:
	type = 'logodds'
assert type == 'logodds' or type == 'ratio'
try:
	min_val = float( sys.argv.pop( 0 ) )
except:
	min_val = 0.001	
try:
	rescale = sys.argv.pop( 0 )
	if rescale.lower()[ 0 ] == 'f': rescale = False
except:
	rescale = False

pssmfile = open( pssmname, 'r' ).readlines()
pssm = load_pssm( pssmfile )
pssm_bgfile = open( pssm_bgname, 'r' ).readlines()
pssm_bg = load_pssm( pssm_bgfile )
if type == 'logodds':
	pssm_out = calc_log_odds_pssm( pssm, pssm_bg, min_val )
elif type == 'ratio':
	pssm_out = calc_ratio_pssm( pssm, pssm_bg, min_val )
if rescale:
	rescale_pssm( pssm, -1., 1. )
print_pssm( pssm_out )
