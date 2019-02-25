#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
try:
	listname = sys.argv.pop( 0 )
except:
	print "args:\tfile_list( or pipe from STDIN )"
	sys.exit()

if listname == '-':
	list = sys.stdin.readlines()
else:
	list = open( listname, 'r' ).readlines()

for filename in list:
	filename = filename.rstrip()
	if not os.path.exists( filename ):
		print filename
