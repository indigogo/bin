#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tfile1\tfile2\theader_tag"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
filename2 = sys.argv.pop( 0 )
mytag = sys.argv.pop( 0 )

file = open( filename, 'r' ).readlines()
file2 = open( filename2, 'r' ).readlines()

#assume line1 == header for both files!
header = file.pop( 0 ).split()
header2_str = file2.pop( 0 )
header2 = header2_str.split()
col = None
for itag in range( len( header ) ):
	tag = header[ itag ]
	if tag == mytag: col = itag
col2 = None
for itag in range( len( header2 ) ):
	tag = header2[ itag ]
	if tag == mytag: col2 = itag
if col2 is None:
	print 'ERROR: header tag', mytag, ' was not found in', filename2, '!!'
	sys.exit()

#warning, assumes unique entries for header_tag values!
#print and continues on first match!
newfile = []
newfile.append( header2_str )
for line in file:
	vals = line.split()
	for line2 in file2:
		vals2 = line2.split()
		if vals2[ col2 ] == vals[ col ]:
			newfile.append( line2 )
			break
		#error if checked line and no match yet
		if line2 == file2[ -1 ]:
			print 'ERROR: value', vals[ col ], ' was not found in', filename2, '!!'
			sys.exit()

os.system( 'cp ' + filename2 + ' ' + filename2 + '.bak' )
newfilehandle = open( filename2, 'w' )
newfilehandle.writelines( newfile )


