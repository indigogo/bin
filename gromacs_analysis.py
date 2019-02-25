#!/usr/bin/python

import sys
import os
import math
import re

if( len( sys.argv ) < 2 ):
	print "args:\tmd.log\tbegin_time\tend_time"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
begin = float( sys.argv.pop( 0 ) )
end = float( sys.argv.pop( 0 ) )

file = open( filename, 'r' ).readlines()
is_frame = re.compile( '\s+Step\s+Time\s+Lambda.*' )
e_pot_corr_avg = 0.
n_frame = 0
while len( file ) > 0:
	line = file.pop( 0 )
	if not is_frame.match( line ): continue
	#get time, skip if out of bounds
	time = float( file.pop( 0 ).split()[ 1 ] )
	if time < begin: continue
	elif time > end: continue
	file.pop( 0 )
	file.pop( 0 )
	file.pop( 0 )
	file.pop( 0 )
	file.pop( 0 )
	#WARNING!! THESE COL INDICES MAY CHANGE!!
	print str( time )
	print file[ 0 ]
	e_posre = float( file.pop( 0 ).split()[ -1 ] )
	file.pop( 0 )
	print file[ 0 ]
	e_pot = float( file.pop( 0 ).split()[ 0 ] )
	e_pot_corr = e_pot - e_posre
	e_pot_corr_avg += e_pot_corr
	n_frame += 1
e_pot_corr_avg /= n_frame
print str( e_pot_corr_avg )
