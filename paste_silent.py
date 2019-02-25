#!/usr/bin/python
# this pastes unique colums from scorefile2 into scorefile 1
# uniqueness of column is based on header tag 
# when header tags match, ignore column from file2
# also matches rows by "description" file2 matches file1

import sys
import os
import re

if( len( sys.argv ) < 2 ):
	print "args:\t*.sc\t*.sc\t<match_tag(description)>\nfirst file takes precedence if matching header tags!"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
filename2 = sys.argv.pop( 0 )
if len( sys.argv ) > 0:
	matchtag = sys.argv.pop( 0 )
else:
	matchtag = 'description'

file = open( filename, 'r' ).readlines()
file2 = open( filename2, 'r' ).readlines()

if len( file ) != len( file2 ):
	print "scorefiles must have same number of rows!"
	sys.exit()

#create dictionary for key->col
header_list = file.pop( 0 ).split()
header = dict( zip( header_list, range( len( header_list ) ) ) )
header_list2 = file2.pop( 0 ).split()
header2 = dict( zip( header_list2, range( len( header_list2 ) ) ) )

#add new tags to output header
for tag in header_list: print tag + '\t',
for key2 in header2.keys():
	if not header.has_key( key2 ): print key2 + '\t',
print

for line in file:
	line = line.rstrip().split()
	desc = line[ header[ matchtag ] ]
	#find entry for file1 line in file2
	for line2 in file2:
		line2 = line2.rstrip().split()
		desc2 = line2[ header2[ matchtag ] ]
		#string match?
		#if not re.match( desc2, desc ): continue
		if desc2 != desc: continue
		for key2 in header2.keys():
			if not header.has_key( key2 ):
				#append new val to line if is unique column
				line.append( line2[ header2[ key2 ] ] )
		break
	for val in line: print val + "\t",
	print


