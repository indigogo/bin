#!/usr/bin/python

### Chris King dr.chris.king@gmail.com
### generate a hostfile for MPI on Bakerlab's dig system

import sys
import os

sys.argv.pop( 0 )
try:
	nametag = sys.argv.pop( 0 )
	inode_low = int( sys.argv.pop( 0 ) )
	inode_hi = int( sys.argv.pop( 0 ) )
except:
	print "args:\tnametag\tdiglow\tdighi\t<ignore_node1,ignore_node2,etc>\n\n"
	sys.exit()
try:
	ignore_nodes = sys.argv.pop( 0 ).split( ',' )
except:
	ignore_nodes = []
nodename_prefix = 'dig'

for inode in range( inode_low, inode_hi + 1 ):
	nodename = nodename_prefix + str( inode )
	if str( inode ) in ignore_nodes: continue
	#round to nearest integer
	print 'pinging', nodename, '...'
	try:
		processes = os.popen( 'ssh -x ' + nodename + ' ps -fu chrisk | grep ' + nametag ).readlines()
		for process in processes:
			pid = process.split()[ 1 ]
			os.popen( 'ssh -x ' + nodename + ' kill ' + pid )
	except: continue


