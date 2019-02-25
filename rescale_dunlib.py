#!/usr/bin/python

import sys
import os
from math import *

if( len( sys.argv ) < 2 ):
	print "args:\tdun_libfile\tdun02||dun08\tprob_temp\tsd_const"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
dunlib = sys.argv.pop( 0 )
p_temp = float( sys.argv.pop( 0 ) )
sd_const = float( sys.argv.pop( 0 ) )

os.system( 'cp ' + filename + ' ' + filename + '.bak' )
zip = False
if filename[ -2: ] == 'gz':
	zip = True
	os.system( 'gzip -d ' + filename )
	filename = filename[ :-3 ]
file = open( filename, 'r' ).readlines()

dun08 = False
if dunlib == dun08: dun08 = True

#TODO:
#how address semi-rotamerics??
newfile = []
bin = []
for i_line in range( len( file ) ):
	line = file[ i_line ]

	if line[ 0 ] == '#':
		newfile.append( line )
		continue
	bin.append( line )
	phipsi = line[ 5:14 ]
	#dont go out of bounds
	if i_line < len( file ) - 1: phipsi_next = file[ i_line + 1 ][ 5:14 ]

	#if at end of bin (or end of file)	
	if phipsi_next != phipsi or i_line == len( file ) - 1:
		z = 0
		ps = []
		#cache rescaled energues and calc partition coeff
		for line in bin:
			if dun08: prob = float( line[ 37:45 ] )
			else: prob = float( line[ 33:41 ] )
			if prob == 0: 
				ps.append( prob )
				continue
			nrg = -log( prob )
			nrg = nrg / p_temp
			p_unnorm = exp( -nrg )
			ps.append( p_unnorm )
			z += p_unnorm

		for line in bin:
			prob = ps.pop( 0 ) / z
			if dun08: newline = line[ :37 ]
			else: newline = line[ :33 ]
			newline += ( "%1.6f" % prob )
			if dun08: newline += ( line[ 45:80 ] )
			else: newline += ( line[ 41:76 ] )

			if dun08: chi1 = float( line[ 80:87 ] )
			else: chi1 = float( line[ 78:85 ] )
			newline += "%7.1f " % ( chi1 * sd_const )

			if dun08: chi2 = float( line[ 89:95 ] )
			else: chi2 = float( line[ 87:93 ] )
			newline += "%7.1f " % ( chi2 * sd_const )

			if dun08: chi3 = float( line[ 96:103 ] )
			else: chi3 = float( line[ 94:101 ] )
			newline += "%7.1f " % ( chi3 * sd_const )

			if dun08: chi4 = float( line[ 104:111 ] )
			else: chi4 = float( line[ 103:109 ] )
			newline += "%7.1f\n" % ( chi4 * sd_const )

			newfile.append( newline )
		bin = []
file = open( filename, 'w' )
file.writelines( newfile )
file.close
if zip == True: os.system( 'gzip ' + filename )

