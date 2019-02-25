#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tcmdline.cmd\tnjobs\tprio\nexpects '=' wildcard in *.cmd file"
	sys.exit()
sys.argv.pop( 0 )
cmdname = sys.argv.pop( 0 )
njobs = int( sys.argv.pop( 0 ) )
prio = sys.argv.pop( 0 )

#read commandline from file
cmd = open( cmdname, 'r' ).readline()
#parse out exec and args
cmdsplit = cmd.split()
exe = cmdsplit.pop( 0 )
args = ' '.join( cmdsplit )
#get jobname
namesplit = cmdname.split( '.' )
namesplit.pop()
name = '.'.join( namesplit )
#and dir
dir = os.getcwd()

print 'universe = vanilla'
print 'notification = Never'
print 'Executable = ' + exe
print 'Initialdir = ' + dir
print 'copy_to_spool = FALSE\n'

for ijob in range( 1, njobs + 1 ):
	args_this = args.replace( '=', str( ijob ) )
	print 'Arguments = ' + args_this
	print 'Output = ' + name + '.' + str( ijob ) + '.out'
	print 'Log = ' + name + '.' + str( ijob ) + '.log'
	print 'Error = ' + name + '.' + str( ijob ) + '.err'
	print 'priority = ' + prio
	print "Queue\n"
