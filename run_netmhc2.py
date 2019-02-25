#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tfasta(s)"
	sys.exit()
sys.argv.pop( 0 )

for fastaname in sys.argv:
	name = '.'.join( fastaname.split( '.' )[ :-1 ] )
	os.system( 'netMHCII -a H-2-IAb -f ' + fastaname + ' > ' + name + '.netmhc2_iab.out' )
