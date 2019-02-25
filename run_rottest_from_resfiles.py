#!/usr/bin/python

#####        run rosetta jobs from resfile list           #######
#################################################################

import os
import sys


if( len( sys.argv ) < 3 ):
	print "args:\tresfilelist\targsfile\trun_name\t<condor>"
	sys.exit()
sys.argv.pop( 0 )
reslistname = sys.argv.pop( 0 )
argsfile = sys.argv.pop( 0 )
runname = sys.argv.pop( 0 )
filesys = sys.argv.pop( 0 )

reslistfile = open( reslistname, 'r' )
reslist = reslistfile.readlines()

app = '/work/chrisk/trunk/mini/bin/rotamer_repack.linuxgccrelease'
path = os.getcwd()

if filesys == 'condor':	
	filename = runname + '.consub'
	consubfile = open( filename, 'w' )
	consubfile.write( 'universe = vanilla\n' )
	consubfile.write( 'notification = Never\n' )
	consubfile.write( 'Executable = ' + app + '\n' )
	consubfile.write( 'Initialdir = ' + path + '\n' )
	consubfile.write( 'Output = ' + runname + '.out\n' )
	consubfile.write( 'Error = ' + runname + '.err\n' )
	consubfile.write( 'Log = ' + runname + '.log\n' )

for i in range( len( reslist ) ):
	resfile = reslist[ i ].rstrip();
	resparse = resfile.split( '.' )
	resparse.pop()
	#n = resparse.pop()
	#nametag = '.'.join( resparse ) + '_' + n
	nametag = '.'.join( resparse ) 
	pdbname = nametag + '.pdb'
	#args = '@' + argsfile + ' -s ' + pdbname + ' -resfile ' + resfile + ' -suffix .' + n
	args = '@' + argsfile + ' -s ' + pdbname + ' -resfile ' + resfile 

	if filesys == 'condor':
		consubfile.write( 'Arguments = ' + args + '\n' )
		consubfile.write( 'Queue\n' )
	else:
		#com = args + ' >& ' + '.'.join( resparse ) + '_' + n + '.out &'
		com = args + ' >& ' + nametag + '.out &'
		os.system( app + ' ' + com )

if filesys == 'condor':
	consubfile.close()
#	os.system( 'condor_submit ' + filename )

reslistfile.close()

