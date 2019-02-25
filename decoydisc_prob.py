#!/usr/bin/python

import sys
import os
import operator


if( len( sys.argv ) < 2 ):
	print "args:\t*.sc\tsort_tag\trmsd_tolerance"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
sort_tag = sys.argv.pop( 0 )
rmsd_tol = float( sys.argv.pop( 0 ) )

def sort_table( table, col = 0 ):
    return sorted( table, key = operator.itemgetter( col ) )

file = open( filename, 'r' ).readlines()

#create dictionary for key->col
header_list = file.pop( 0 ).split()
header = dict( zip( header_list, range( len( header_list ) ) ) )

#name_col = header[ 'description' ]
rmsd_col = header[ 'rms' ]
sort_col = header[ sort_tag ]
#empty 2D list
rmsd_sortval = [ ]
#fill list with [rmsd,sortval] pairs
for line in file:
	vals = line.split()
	rmsd_sortval.append( [ float( vals[ rmsd_col ] ), float( vals[ sort_col ] ) ] )

#sort by sortval
rmsd_sortval = sort_table( rmsd_sortval, 1 )
#print rmsd_sortval

#calc % of decoys needed to sample under rmsd_tol
n_low = 0.
for decoy in rmsd_sortval:
	n_low += 1.
	if decoy[ 0 ] < rmsd_tol: break
sample_frac = ( n_low / len( rmsd_sortval ) )
print filename, sort_tag, str( rmsd_tol ) + ':\t' + str( sample_frac )
