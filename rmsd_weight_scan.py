#!/usr/local/bin/python

import sys
import os
import math
import numpy
from numpy import *

if( len( sys.argv ) < 2 ):
	print "args:\tfile\tcol1\tcol2\twt_min\twt_delta\twt_max"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
col1 = int( sys.argv.pop( 0 ) )
col2 = int( sys.argv.pop( 0 ) )
wt_min = float( sys.argv.pop( 0 ) )
wt_d = float( sys.argv.pop( 0 ) )
wt_max = float( sys.argv.pop( 0 ) )

data = genfromtxt( filename )
ref = data[ :, col1-1 ]
test = data[ :, col2-1 ]
rmsd_min = None
wt_opt = None
wts = arange( wt_min, (wt_max + wt_d), wt_d ) 
for wt in wts:
	test_wtd = test * wt
	rmsd = sqrt( average( ( ref - test_wtd )**2 ) )
	if rmsd_min == None:
		rmsd_min = rmsd
		wt_opt = wt
	elif rmsd < rmsd_min:
		rmsd_min = rmsd
		wt_opt = wt
print 'rmsd:', str(rmsd_min), 'weight:', str(wt_opt)
