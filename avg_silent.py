#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tscorefile\t<read_all_lines>"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
if len( sys.argv ) > 0: read_all = True
else: read_all = False

file = open( filename, 'r' ).readlines()
name = '.'.join( filename.split( '.' )[ :-1 ] )

#get header, first line that begins "SCORE:"
while True:
	header_str  = file.pop( 0 )
	if header_str.split()[ 0 ] == 'SCORE:' or read_all: break

#header is tag list
header = header_str.split()

#sum vals in text file
sc_avg = [ 0 ] * len( header )
sc_nlines = 0
for line in file:
	sc_line = line.split()
	if sc_line[ 0 ] != 'SCORE:' and not read_all: continue
	#feh hack to skip over double headers
	if sc_line[ 1 ] == 'score': continue
	sc_nlines += 1
	for ival in range( len( sc_line ) ):
		try: sc_avg[ ival ] += float( sc_line[ ival ] )
		except ValueError:
			if sc_line[ ival ] == 'SCORE:': sc_avg[ ival ] = sc_line[ ival ]
			else: sc_avg[ ival ] = name

#print header?
print header_str,

#now divide by nlines
for val in sc_avg:
	try:
		val = val / sc_nlines
		print '%.3f' % val,
	except:
		print val,
print


