#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tscorefile\tn_rms_bins\tn_structs\t<rmsd_tag(rms)>\t<score_tag(score)>\t<read_all>"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
n_rms_bins = int( sys.argv.pop( 0 ) )
nstruct = int( sys.argv.pop( 0 ) )
if len( sys.argv ) > 0:
	rmsd_tag = sys.argv.pop( 0 )
else: rmsd_tag = 'rms'
if len( sys.argv ) > 0:
	score_tag = sys.argv.pop( 0 )
else: score_tag = 'score'
if len( sys.argv ) > 0:
	read_all = sys.argv.pop( 0 )
else: read_all = False

file = open( filename, 'r' ).readlines()

#get header, first line that begins "SCORE:"
while True:
	header_str  = file.pop( 0 )
	if header_str.split()[ 0 ] == 'SCORE:' or read_all: break

#get col nums for score, rms
header = dict( zip( header_str.split(), range( len( header_str.split() ) ) ) )

#convert text file to data
scdata = []
for line in file:
	line_parse = line.split()
	if line_parse[ 0 ] != 'SCORE:' and not read_all: continue
	#feh hack to skip over double headers
	if line_parse[ 1 ] == 'score': continue
	line_data = []
	for val in line_parse:
		try: line_data.append( float( val ) )
		except ValueError: line_data.append( val )
	#check type to skip broken lines
	if len( line_data ) < header[ rmsd_tag ] or len( line_data ) < header[ score_tag ]:
		print 'line too short at line:\n', line
		sys.exit()
	if not type( line_data[ header[ rmsd_tag ] ] ) is float: continue
	if not type( line_data[ header[ score_tag ] ] ) is float: continue
	scdata.append( line_data )

#sort by rms
scdata = sorted( scdata, key=lambda scdata: scdata[ header[ rmsd_tag ] ] )

#get min, max rms
min_rms = scdata[ 0 ][ header[ rmsd_tag ] ]
max_rms = scdata[ -1 ][ header[ rmsd_tag ] ]
try: d_rms = ( max_rms - min_rms ) / ( n_rms_bins )
except:
	print max_rms, 'or', min_rms, 'are not a number!'
	sys.exit()
max_bin_rms = []
rms = min_rms
while rms < max_rms:
	rms += d_rms
	max_bin_rms.append( rms )

#print header
print header_str,

bin_scdata = []
irms = 0
while len( scdata ) > 0:
	#move data from all data into bin data
	bin_scdata.append( scdata.pop( 0 ) )
	#if rms exceeds max bin rms, sort, filter, print
	if bin_scdata[ -1 ][ header[ rmsd_tag ] ] >= max_bin_rms[ irms ]:
		#sort by score
		bin_scdata = sorted( bin_scdata, key=lambda bin_scdata: bin_scdata[ header[ score_tag ] ] )
		#filter and print lowest n_struct lines
		if nstruct < len( bin_scdata ): bin_scdata =  bin_scdata[ :nstruct ]
		for struct in bin_scdata:
			for val in struct:
				print str( val ),
			print
		#increment max rms iter and reinit bin data
		irms += 1
		bin_scdata = []

