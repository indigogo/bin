#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tcmdline.cmd\tlist\tlist2\tprio\n'=' list wildcard, '*' list2 wildcard in *.cmd file"
	sys.exit()
sys.argv.pop( 0 )
cmdname = sys.argv.pop( 0 )
listname = sys.argv.pop( 0 )
listname2 = sys.argv.pop( 0 )
prio = sys.argv.pop( 0 )

#read commandline from file
cmd = open( cmdname, 'r' ).readline()
list = open( listname, 'r' ).readlines()
list2 = open( listname2, 'r' ).readlines()
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
	args_job = args.replace( '=', job )
	for job2 in list2:
		job2 = job2.rstrip()
		args_job2 = args_job.replace( '*', job2 )
		print 'Arguments = ' + args_job2
		print 'Output = ' + job + '.' + name + '.' + job2 + '.out'
		print 'Log = ' + job + '.' + name + '.' + job2 + '.log'
		print 'Error = ' + job + '.' + name + '.' + job2 + '.err'
		print 'priority = ' + prio
		print "Queue\n"
