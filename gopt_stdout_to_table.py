#!/usr/bin/python

import sys
import os
import re

aa3s = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']
aa1s= [ 'A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V' ] 

sys.argv.pop( 0 )
if len( sys.argv ) < 1:
	print "args:\t"
	sys.exit()
filenames = sys.argv

tracer = re.compile( 'protocols.design_opt.PointMutationCalculator:.* Mutation [A-Z]_\d+_[A-Z]' )

data = {}
for filename in filenames:
	filename = filename.rstrip()
	file = open( filename, 'r' ).readlines()
	for line in file:
		if not tracer.match( line ): continue;
		line = line.rstrip().split()
		mut = line[ 3 ]
		seqpos = int( mut.split( '_' )[ 1 ] )
		aa1 = mut.split( '_' )[ 2 ]
		aa3 = aa3s[ aa1s.index( aa1 ) ]
		if mut[ 0 ] == mut[ -1 ]: aa3 = aa3 + '*'
		score  = line[ -2 ]
		if not data.has_key( seqpos ): data[ seqpos ] = {}
		data[ seqpos ][ aa3 ] = score

for seqpos in sorted( data.iterkeys() ):	
	print str( seqpos ), '(' + str( seqpos ) + ' C)\t',
	for aa3 in sorted( data[ seqpos ].iterkeys() ):
		print aa3 + ':' + data[ seqpos ][ aa3 ],
	print 
