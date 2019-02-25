#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tsilentfile\ttaglist"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
taglistname = sys.argv.pop( 0 )

file = open( filename, 'r' ).readlines()
name = '.'.join( filename.split( '.' )[ :-1 ] )
taglist = open( taglistname, 'r' ).readlines()

#put tags in a list
tags = []
for tag in taglist:
	tag = tag.rstrip()
	tags.append( tag )

#get header, first line that begins "SCORE:"
while True:
	header_str  = file.pop( 0 )
	print header_str,
	if header_str.split()[ 0 ] == 'SCORE:': break

#header is tag dict
header_list = header_str.split()
header = dict( zip( header_list, range( len( header_list ) ) ) )

#go thru each line
#if is score line, check tag
#if tag in taglist, start printing until next score line
printing = False
for line in file:
	line = line.rstrip()
	parse = line.split()
	if parse[ 0 ] == 'SCORE:':
		tag = parse[ header[ 'description' ] ]
		if tag in tags: printing = True
		else: printing = False
	if printing: print line

