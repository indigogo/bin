#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tsilentfile\ttaglist"
	sys.exit()
sys.argv.pop( 0 )
silentfilename = sys.argv.pop( 0 )
tagfilename = sys.argv.pop( 0 )
silentfile = open( silentfilename, 'r' ).readlines()
tagfile = open( tagfilename, 'r' ).readlines()

i_name = 0
for silentline in silentfile:
	parse = silentline.rstrip().split()
	if parse[ 0 ] != 'SCORE:': continue
	#if is header, print it, find name colum, and break
	if parse[ 1 ] == 'score':
		print silentline,
		for i in range( len( parse ) ): 
			if parse[ i ] == 'description': i_name = i
		break
#over each name in taglist
for tagline in tagfile:
	tagline = tagline.rstrip()
	#over each score line in silent file
	for silentline in silentfile:
		parse = silentline.rstrip().split()
		if parse[ 0 ] != 'SCORE:': continue
		#if is header, find col idx for name
		if parse[ 1 ] == 'score':
			continue
		name = parse[ i_name ]
		if tagline == name:
			print silentline,
			continue
