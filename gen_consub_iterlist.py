#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tcmdline.cmd\tlist\tn_iter\tprio\n'=' list wildcard, '*' iter wildcard in *.cmd file"
	sys.exit()
sys.argv.pop( 0 )
cmdname = sys.argv.pop( 0 )
listname = sys.argv.pop( 0 )
n_iter = int( sys.argv.pop( 0 ) )
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
	args_job = args.replace( '=', job )
	for iter in range( 1, n_iter + 1 ):
		args_job_iter = args_job.replace( '*', str( iter ) )
		print 'Arguments = ' + args_job_iter
		print 'Output = ' + job + '.' + name + '.' + str( iter ) + '.out'
		print 'Log = ' + job + '.' + name + '.' + str( iter ) + '.log'
		print 'Error = ' + job + '.' + name + '.' + str( iter ) + '.err'
		print 'priority = ' + prio
		print "Queue\n"
