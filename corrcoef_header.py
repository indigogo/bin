#!/usr/local/bin/python

import sys
import os
import math
import numpy

if( len( sys.argv ) < 2 ):
	print "args:\tfile\ttag1\ttag2"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
tag1 = sys.argv.pop( 0 )
tag2 = sys.argv.pop( 0 )

header = open( filename, 'r' ).readline().split()
headerdict = dict( zip( header, range( len( header ) ) ) )
data = numpy.genfromtxt( filename, skip_header = 1 )
corrmat = numpy.corrcoef( data[ :, headerdict[ tag1 ] ], data[ :, headerdict[ tag2 ] ], rowvar=0 )
corr = corrmat[ 0, 1 ]

print corr
