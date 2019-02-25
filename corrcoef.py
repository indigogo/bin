#!/usr/local/bin/python

import sys
import os
import math
import numpy

if( len( sys.argv ) < 2 ):
	print "args:\tfile\tcol1(1)\tcol2(2)"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
if len( sys.argv ) > 0: col1 = int( sys.argv.pop( 0 ) )
else: col1 = 1
if len( sys.argv ) > 0: col2 = int( sys.argv.pop( 0 ) )
else: col2 = 2

data = numpy.genfromtxt( filename )
corrmat = numpy.corrcoef( data[ :, col1-1 ], data[ :, col2-1 ], rowvar=0 )
corr = corrmat[ 0, 1 ]

print corr
