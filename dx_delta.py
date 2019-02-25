#!/usr/bin/python

import sys
import os
import math
import time

if( len( sys.argv ) < 2 ):
	print "args:\tdxfile1\tdxfile2"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
filename2 = sys.argv.pop( 0 )

file = open( filename, 'r' ).readlines()
file2 = open( filename2, 'r' ).readlines()
#load array w/ important data, check if consistent
header = []
header2 = []

line = file.pop( 0 )
print line,
parse = line.split()
header.append( parse[ 5 ] )
header.append( parse[ 6 ] )
header.append( parse[ 7 ] )
line = file.pop( 0 )
print line,
parse = line.split()
header.append( parse[ 1 ] )
header.append( parse[ 2 ] )
header.append( parse[ 3 ] )
line = file.pop( 0 )
print line,
parse = line.split()
header.append( parse[ 1 ] )
line = file.pop( 0 )
print line,
parse = line.split()
header.append( parse[ 2 ] )
line = file.pop( 0 )
print line,
parse = line.split()
header.append( parse[ 3 ] )
line = file.pop( 0 )
print line,
line = file.pop( 0 )
print line,
parse = line.split()
header.append( parse[ 9 ] )

parse = file2.pop( 0 ).split()
header2.append( parse[ 5 ] )
header2.append( parse[ 6 ] )
header2.append( parse[ 7 ] )
parse = file2.pop( 0 ).split()
header2.append( parse[ 1 ] )
header2.append( parse[ 2 ] )
header2.append( parse[ 3 ] )
parse = file2.pop( 0 ).split()
header2.append( parse[ 1 ] )
parse = file2.pop( 0 ).split()
header2.append( parse[ 2 ] )
parse = file2.pop( 0 ).split()
header2.append( parse[ 3 ] )
file2.pop( 0 )
parse = file2.pop( 0 ).split()
header2.append( parse[ 9 ] )

for iheader in range( len( header ) ):
	if header[ iheader ] != header2[ iheader ]:
		print "header mismatch!", header[ iheader ], ":", header2[ iheader ]
		time.sleep( 1.0 )

#now diff files
while len( file ) > 1:
	parse = file.pop( 0 ).split()
	parse2 = file2.pop( 0 ).split()
	#"    0.99992E+000    0.10001E+001    0.99997E+000"
	for ival in range( len( parse ) ):
		dval = float( parse2[ ival ] ) - float( parse[ ival ] )
		print "   " + "%.5E" % dval,
	print
