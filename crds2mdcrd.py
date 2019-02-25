#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tprmtop\ttag.crdlist"
	sys.exit()
sys.argv.pop( 0 )
prmtopname = sys.argv.pop( 0 )
crdlistname = sys.argv.pop( 0 )
crdlist = open( crdlistname, 'r' ).readlines()
baselistname = crdlistname.replace( '.crdlist', '' )

#ptraj file
ptrajfile = open( baselistname + '.ptraj.in', 'w' )
for crdname in crdlist:
	crdname = crdname.rstrip()

	#add to ptraj file
	ptrajfile.write( 'trajin ' + crdname + '\n' )

ptrajfile.write( 'trajout ' + baselistname + '.mdcrd trajectory nobox\ngo\n' )
ptrajfile.close()
os.system( '/work/chrisk/amber11/bin/ptraj ' + prmtopname + ' ' + baselistname + '.ptraj.in' )
