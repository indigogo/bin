#!/usr/bin/python

import sys
import os
import re

if( len( sys.argv ) < 2 ):
	print "args:\tref_netmhcII_output\ttest_netmhcII_output\t<cutoff(SB|WB|value)>"
	sys.exit()
sys.argv.pop( 0 )
ref_mhcname = sys.argv.pop( 0 )
mhcname = sys.argv.pop( 0 )
if len( sys.argv ) > 0: cutoff = sys.argv.pop( 0 )
else: cutoff = 'SB'
if len( sys.argv ) > 0: chain = sys.argv.pop( 0 )
else: chain = None
ep_len = 9

ref_mhc = open( ref_mhcname, 'r' ).readlines()
mhc = open( mhcname, 'r' ).readlines()

# regex to find netmhc data lines w/ binders
epline_str = '.*\S+\s+\d+\s+[A-Z]+\s+[A-Z]+\s+\d+\.\d+\s+\d+\.\d+\s+'
ref_epline_str = '.*\S+\s+\d+\s+[A-Z]+\s+[A-Z]+\s+\d+\.\d+\s+\d+\.\d+\s+'
# numerical cutoff or WB/SB match?
try:
	cutoff = float( cutoff )
	num_cut = True
except:
	num_cut = False
	#incl weak binders?
	if cutoff == 'WB':
		ref_epline_str += '[WS]B' 
	elif cutoff == 'SB':
		ref_epline_str += 'SB'
#else matches all lines 
ref_epline = re.compile( ref_epline_str )
epline = re.compile( epline_str )

#find all mhc 9mers indexed by netmhc output in ref file
ref_epi_allele_datamap = {}
for il,line in enumerate( ref_mhc ):
	if not ref_epline.match( line ): continue
	line = line.rstrip().split()
	ic50 = float( line[ 5 ] )
	if num_cut and ic50 > cutoff: continue
	ires_nmer = int( line[ 1 ] )
	allele = line[ 0 ].replace( '-', '' ).lower()
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
	ref_epi_allele_data = ( allele, ires_core, core )
	#only add to list if isn't already there OR if ic50 is lower
	if not ref_epi_allele_datamap.has_key( ref_epi_allele_data ):
		ref_epi_allele_datamap[ ref_epi_allele_data ] = [ ic50, core ]
	elif ref_epi_allele_datamap[ ref_epi_allele_data ] > ic50:
		ref_epi_allele_datamap[ ref_epi_allele_data ] = [ ic50, core ]

#find all matching mhc 9mers in other seq
epi_allele_datamap = {}
for il,line in enumerate( mhc ):
	if not epline.match( line ): continue
	line = line.rstrip().split()
	ic50 = float( line[ 5 ] )
	ires_nmer = int( line[ 1 ] )
	allele = line[ 0 ].replace( '-', '' ).lower()
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
	#now see if we have an epitope stored whose index fits within this 15mer
	for ref_epi_allele_data in ref_epi_allele_datamap.iterkeys():
		ref_allele = ref_epi_allele_data[ 0 ]
		ref_ires_core = ref_epi_allele_data[ 1 ]
		#index in 15mer is between 1 and 6?
		if ref_allele == allele and ref_ires_core >= ires_nmer and ref_ires_core <= ires_nmer + 6:
			if not epi_allele_datamap.has_key( ref_epi_allele_data ):
				epi_allele_datamap[ ref_epi_allele_data ] = [ ic50, core ]
			#replace it if we have a lower ic50
			elif epi_allele_datamap[ ref_epi_allele_data ] > ic50:
				epi_allele_datamap[ ref_epi_allele_data ] = [ ic50, core ]
			
#iter over ref keys because we may not have aded the matching one if it never got picked as a 9mer core
for ikey, epi_allele_data in enumerate( sorted( epi_allele_datamap.iterkeys() ) ):
	#skip if no change in IC50 or sequence
	if ref_epi_allele_datamap[ epi_allele_data ][ 0 ] == epi_allele_datamap[ epi_allele_data ][ 0 ] and epi_allele_data[ 2 ] == epi_allele_datamap[ epi_allele_data ][ 1 ]: continue
	print epi_allele_data[ 0 ] + ' ' + str( epi_allele_data[ 1 ] ) + ' ' + str( epi_allele_data[ 2 ] ) + ' ' + str( ref_epi_allele_datamap[ epi_allele_data ][ 0 ] ) + ' -> ' + epi_allele_datamap[ epi_allele_data ][ 1 ], str( epi_allele_datamap[ epi_allele_data ][ 0 ] )
#		print epi_allele_data[ 0 ] + ' ' + str( epi_allele_data[ 1 ] ) , str( epi_allele_datamap[ epi_allele_data ][ 0 ] )

