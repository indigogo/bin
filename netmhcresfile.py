#!/usr/bin/python

import sys
import os
import re

if( len( sys.argv ) < 2 ):
	print "args:\tnetmhcII_output\tpdbfile\t<cutoff(SB|WB|value)>\t<pdb_chain>"
	sys.exit()
sys.argv.pop( 0 )
mhcname = sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
if len( sys.argv ) > 0: cutoff = sys.argv.pop( 0 )
else: cutoff = 'SB'
if len( sys.argv ) > 0: chain = sys.argv.pop( 0 )
else: chain = None
ep_len = 9

pdb = open( pdbname, 'r' ).readlines()
mhc = open( mhcname, 'r' ).readlines()

# regex to find netmhc data lines w/ binders
epline_str = '.*\d+\s+[A-Z]+\s+\d+\.\d+\s+\d+\s+'
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

#find all mhc 9mers indexed by netmhc output
epis = []
for il,line in enumerate( mhc ):
	if not epline.match( line ): continue
	line = line.rstrip().split()
	ic50 = float( line[ 3 ] )
	if num_cut and ic50 > cutoff: continue
	ires_nmer = int( line[ 0 ] )
	nmer = line[ 1 ]
	core = line[ 1 ]
	ires_core = None
	#find res index of 9mer core
	for iseq in range( len( nmer ) - len( core ) + 1 ):
		if nmer[ iseq:( len( core ) + iseq ) ] == core:
			ires_core = ires_nmer + iseq
			break
	if ires_core is None:
		print "ERROR: 9mer ", core, "not found in seq ", nmer, "at line", il
		sys.exit()
	for iseq in range( ep_len ):
		if not ires_core in epis: epis.append( ires_core )
		ires_core += 1
	
#now match ep res indices to pdb indices, need nterm offset
#this will break only if pdb is missing nterm epitopes
ires1_pdb = None
pdb_res = []
for il,line in enumerate( pdb ):
	if not line.startswith( 'ATOM' ): continue
	if chain is None: chain = line[ 21 ]
	elif line[ 21 ] != chain: continue
	#store res index of existing residue (in case of missing res)
	ires_pdb = int( line[ 22:26 ].strip() )
	if ires_pdb not in pdb_res: pdb_res.append( ires_pdb )
	if ires1_pdb is None:
		ires1_pdb = ires_pdb

#output resfile
#need to rename blank chain id
if chain == ' ': chain = '_'
print 'NATAA\nstart'	
for epi in sorted( epis ):
	ires_ep_pdb = epi + ires1_pdb
	if ires_ep_pdb not in pdb_res: continue
	print str( ires_ep_pdb ), chain, 'ALLAAxc'
