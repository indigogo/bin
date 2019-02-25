#!/usr/bin/python

import sys
import os
import math

#takes 2 lists of strings, returns sum
def sum_lines( l1, l2 ):
	ltot = l1
	for ival in range( len( l2 ) ):
		try:
			ltot[ ival ] = str( float( l1[ ival ] ) + float( l2[ ival ] ) )
		except:
			ltot[ ival ] = ltot[ ival ]
	return ltot

if( len( sys.argv ) < 2 ):
	print "args:\t*.byres.sc\tavg_tag"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
avg_tag = sys.argv.pop( 0 )

file = open( filename, 'r' ).readlines()

#create dictionary for key->col
header_list = file.pop( 0 ).split()
header = dict( zip( header_list, range( len( header_list ) ) ) )

#name_col = header[ 'description' ]
avg_col = header[ avg_tag ]
#empty dictionary
val_sums = {}
val_ns = {}
#sum lines into diff lists spec by avg'ing col val
for line in file:
	vals = line.split()
#	name = vals[ name_col ]
	avg_val = vals[ avg_col ]

	#accumulate line vals into sum list for that avg key
	if val_sums.has_key( avg_val ):
		val_sums[ avg_val ] = sum_lines( val_sums[ avg_val ], vals )
		val_ns[ avg_val ] += 1
	else:
		val_sums[ avg_val ] = vals
		val_ns[ avg_val ] = 1

for tag in header_list:
	print tag, "\t",
print
try:
	tags = sorted( val_sums.keys(), key = lambda a:map( int, a.split( '.' ) ) )
except:
	tags = sorted( val_sums.keys() )
#for tag in sorted( val_sums.keys() ):
for tag in tags:
	vals = val_sums[ tag ]
	for val in vals:
		try:
			avg_val = float( val ) / val_ns[ tag ]
			print "%.3f" % avg_val,
			print "\t",
		except:
			avg_val = val
			print avg_val, "\t",
	print
