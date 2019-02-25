#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tcmdline.cmd\tlist\tprio\nexpects '=' wildcard in *.cmd file"
	sys.exit()
sys.argv.pop( 0 )
cmdname = sys.argv.pop( 0 )
listname = sys.argv.pop( 0 )
prio = sys.argv.pop( 0 )

#read commandline from file
cmd = open( cmdname, 'r' ).readline()
list = open( listname, 'r' ).readlines()
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

for job in list:
	job = job.rstrip()
	args_this = args.replace( '=', job )
	print 'Arguments = ' + args_this
	print 'Output = ' + job + '.' + name + '.out'
	print 'Log = ' + job + '.' + name + '.log'
	print 'Error = ' + job + '.' + name + '.err'
	print 'priority = ' + prio
	print "Queue\n"
