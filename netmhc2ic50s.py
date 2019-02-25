#!/usr/bin/python

import sys
import os
import re

if( len( sys.argv ) < 2 ):
	print "args:\tref_netmhcII_output\t<cutoff(SB|WB|value)>"
	sys.exit()
sys.argv.pop( 0 )
ref_mhcname = sys.argv.pop( 0 )
if len( sys.argv ) > 0: cutoff = sys.argv.pop( 0 )
else: cutoff = 'SB'
if len( sys.argv ) > 0: chain = sys.argv.pop( 0 )
else: chain = None
ep_len = 9

ref_mhc = open( ref_mhcname, 'r' ).readlines()

# regex to find netmhc data lines w/ binders
epline_str = '.*\S+\s+\d+\s+[A-Z]+\s+[A-Z]+\s+\d+\.\d+\s+\d+\.\d+\s+'
# numerical cutoff or WB/SB match?
try:
	cutoff = float( cutoff )
	num_cut = True
except:
	num_cut = False
	#incl weak binders?
	if cutoff == 'WB':
		epline_str += '[WS]B' 
	elif cutoff == 'SB':
		epline_str += 'SB'
#else matches all lines 
epline = re.compile( epline_str )

#find all mhc 9mers indexed by netmhc output in ref file
epi_allele_datamap = {}
for il,line in enumerate( ref_mhc ):
	if not epline.match( line ): continue
	line = line.rstrip().split()
	ic50 = float( line[ 5 ] )
	if num_cut and ic50 > cutoff: continue
	ires_nmer = int( line[ 1 ] )
	allele = line[ 0 ]
	nmer = line[ 2 ]
	core = line[ 3 ]
	ires_core = None
	#find first res index of 9mer core inside bigger nmer epitope
	for iseq in range( len( nmer ) - len( core ) + 1 ):
		if nmer[ iseq:( len( core ) + iseq ) ] == core:
			ires_core = ires_nmer + iseq
			break
	if ires_core is None:
		print "ERROR: 9mer ", core, "not found in seq ", nmer, "at line", il
		sys.exit()
	#store tuple of allele name and core index as key to ic50
	epi_allele_data = ( allele, ires_core )
	#only add to list if isn't already there OR if ic50 is lower
	if not epi_allele_datamap.has_key( epi_allele_data ):
		epi_allele_datamap[ epi_allele_data ] = ic50
	elif epi_allele_datamap[ epi_allele_data ] > ic50:
		epi_allele_datamap[ epi_allele_data ] = ic50

for epi_allele_data in epi_allele_datamap.iterkeys():
	print epi_allele_data[ 0 ], epi_allele_data[ 1 ], str( epi_allele_datamap[ epi_allele_data ] )
