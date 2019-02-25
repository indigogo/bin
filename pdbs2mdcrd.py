#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\t\"name\".pdblist"
	sys.exit()
sys.argv.pop( 0 )
pdblistname = sys.argv.pop( 0 )
pdblist = open( pdblistname, 'r' ).readlines()
baselistname = pdblistname.replace( '.pdblist', '' )

#leap file, 
leapfile = open( baselistname + '.leap.in', 'w' )
#USING ff03.r1 FORCEFIELD!
leapfile.write( 'source /work/chrisk/amber11/dat/leap/cmd/leaprc.ff03.r1\n' )
#ptraj file
ptrajfile = open( baselistname + '.ptraj.in', 'w' )
for pdbname in pdblist:
	pdbname = pdbname.rstrip()
	basename = pdbname.replace( '.pdb', '' )

	#run clean_pdb.pl, should be function up top
	os.system( '/work/chrisk/bin/clean_pdb.pl ' + pdbname )
	#YEAH I JUST CALLED A PERL SCRIPT FROM A PYTHON SCRIPT WHAT?!

	#add to leap file
	leapfile.write( 's = loadPdb ' + basename + '.clean.pdb\n' )
	leapfile.write( 'saveAmberParm s ' + baselistname + '.prmtop ' + basename + '.crd\n' )

	#add to ptraj file
	ptrajfile.write( 'trajin ' + basename + '.crd\n' )

leapfile.write( 'quit\n' )	
ptrajfile.write( 'trajout ' + baselistname + '.mdcrd trajectory nobox\ngo\n' )

leapfile.close()
ptrajfile.close()

#run leap >& leap.out
os.system( '/work/chrisk/amber11/bin/tleap -f ' + baselistname + '.leap.in >& ' + baselistname + '.leap.out' )
#run ptraj >& ptraj.out
os.system( '/work/chrisk/amber11/bin/ptraj ' + baselistname + '.prmtop ' + baselistname + '.ptraj.in >& ' + baselistname + '.ptraj.out' )

