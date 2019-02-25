#!/usr/bin/python

import sys
import os
import math
from gogolib import aa3_to_aa1

#takes 2 lists of strings, returns sum
def sum_lines( l1, l2, ignore_cols ):
	ltot = l1
	for ival in range( len( l2 ) ):
		if ival in ignore_cols: continue
		try:
			ltot[ ival ] = str( float( l1[ ival ] ) + float( l2[ ival ] ) )
		except:
			ltot[ ival ] = ltot[ ival ]
	return ltot

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	window_size = int( sys.argv.pop( 0 ) )
except:
	print "args:\t*.byres.sc\twindow_size"
	sys.exit()

file = open( filename, 'r' ).readlines()

#create dictionary for key->col
header_list = file.pop( 0 ).split()
header_dict = dict( zip( header_list, range( len( header_list ) ) ) )
#dont avg vals in these columns
noavg_tags = [ 'seqpos', 'pdbname', 'pdb_chain', 'pdb_resnum', 'aaidx', 'aa', 'description' ]
noavg_tag_cols = []
for tag in noavg_tags: noavg_tag_cols.append( header_dict[ tag ] )  

#empty list
val_sums = []
#sum lines into diff lists spec by avg'ing col val
for il in range( len( file ) - window_size + 1 ):
	subseq = ''
	for iw in range( window_size ):
		line = file[ il + iw ]
		vals = line.split()
		try: 
			subseq += aa3_to_aa1[ vals[ header_dict[ 'aa' ] ] ]
		except:
			subseq += 'X'
		#accumulate line vals into sum list for that avg key
		try:
			val_sums[ il ] = sum_lines( val_sums[ il ], vals, noavg_tag_cols )
		except:
			val_sums.append( vals )
	val_sums[ -1 ].append( subseq )
header_list.append( 'seq' + str( window_size) )

for tag in header_list:
	print tag, "\t",
print
for vals in val_sums:
	for ival, val in enumerate( vals ):
		if ival in noavg_tag_cols:
			print str( val ), '\t',
		else:
			try:
				avg_val = float( val ) / window_size
				print "%.3f" % avg_val,
				print "\t",
			except:
				avg_val = val
				print avg_val, "\t",
	print
