#!/usr/bin/python

#####        run rosetta jobs from resfile list           #######
#################################################################

import os
import sys

if( len( sys.argv ) < 2 ):
	print "args:\tresfile_list\targsfile\t<condor>"
	sys.exit()
sys.argv.pop( 0 )
reslistname = sys.argv.pop( 0 )
argsfile = sys.argv.pop( 0 )
filesys = sys.argv.pop( 0 )

def submit_condor_job( path, app, nametag, args ):
	filename = nametag + '.consub'
	consubfile = open( filename, 'w' )
	consubfile.write( 'universe = vanilla\n' )
	consubfile.write( 'notification = Never\n' )
	consubfile.write( 'Executable = ' + app + '\n' )
	consubfile.write( 'Arguments = ' + args + '\n' )
	consubfile.write( 'Initialdir = ' + path + '\n' )
	consubfile.write( 'Output = ' + nametag + '.out\n' )
	consubfile.write( 'Error = ' + nametag + '.err\n' )
	consubfile.write( 'Log = ' + nametag + '.log\n' )
	consubfile.close()
	os.system( 'condor_submit ' + filename )

reslistfile = open( reslistname, 'r' )
reslist = reslistfile.readlines()

app = '/work/chrisk/trunk/mini/bin/rotamer_analysis.linuxgccrelease'
path = os.getcwd()

for i in range( len( reslist ) ):
	resfile = reslist[ i ].rstrip();
	resparse = resfile.split( '.' )
	resparse.pop()
	n = resparse.pop()
	native_pdbname = '.'.join( resparse ) + '.pdb'
	pdbname = '.'.join( resparse ) + '.' + n + '_0001.pdb'
	args = '@' + argsfile + ' -s ' + pdbname + ' -resfile ' + resfile + ' -native ' + native_pdbname + ' -mute all -unmute apps.pilot.chrisk.rotamer_analysis'

	if filesys == 'condor':
		submit_condor_job( path, app, nametag, args )
	else:
		com = args + ' >& ' + '.'.join( resparse ) + '_' + n + '.anl &'
		os.system( app + ' ' + com )

reslistfile.close()

