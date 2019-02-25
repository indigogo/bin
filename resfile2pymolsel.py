#!/usr/bin/python

import sys
import os
import re

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
except:
	print "args:\tresfile"
	sys.exit()

if filename == '-':
	file = sys.stdin.readlines()
	filename = 'qq'
else:
	file = open( filename, 'r' ).readlines()

rxp = re.compile( '^\s*\d+\s+[A-Z]\s+' ) #WARNING this will fail with weird chain ID's (e.g. _ or *)
sys.stdout.write( 'select ' + '.'.join( filename.split( '/' )[ -1 ] ) + ', ' )
for line in file:
	if not rxp.match( line ): continue
	toks = line.rstrip().split()
	sys.stdout.write( 'resi ' + toks[ 0 ] + ' and chain ' + toks[ 1 ] + ' ' )
	if line != file[ -1 ]: sys.stdout.write( 'or ' )
sys.stdout.write( '\n' )
