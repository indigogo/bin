#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tsilentfile\tn_slices"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
n_slice = int( sys.argv.pop( 0 ) )

file = open( filename, 'r' ).readlines()
#filename_tag = '.'.join( filename.split( '.' )[ :-1 ] ) 

#find n_decoys
n_struct = 0
for line in file:
	if line[ 0:19 ] == 'ANNOTATED_SEQUENCE:': n_struct += 1

#calc n_decoys_slice, remain
n_struct_slice = int( n_struct / n_slice )
n_struct_remain = n_struct - n_struct_slice * n_slice

#loop over remain, distribute until gone
n_structs = [ n_struct_slice ] * n_slice
islice = 0
while n_struct_remain > 0:
	n_structs[ islice ] += 1
	n_struct_remain -= 1
	islice = ( islice + 1 ) % ( n_slice - 1 )

#get header
header = []
header.append( file.pop( 0 ) )
header.append( file.pop( 0 ) )

#print n_struct_this structures to each slice
iline = 0
for islice in range( len( n_structs ) ):
	n_struct_this = n_structs[ islice ]
	#open new file
	slice_out_name = filename + '.' + str( n_slice ) + '.' + str( islice + 1 )
	slice_out = open( slice_out_name, 'w' )
	#print header
	slice_out.writelines( header )
	#print structs
	n_struct_assigned = 0
	while iline <= len( file ) - 1:
		line = file[ iline ]
		if line[ 0:6 ] == 'SCORE:': n_struct_assigned += 1
		if n_struct_assigned > n_struct_this: break
		iline += 1
		slice_out.write( line )
	slice_out.close()
	
