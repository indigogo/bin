#!/usr/bin/python

### Chris King dr.chris.king@gmail.com
### generate a hostfile for MPI on Bakerlab's dig system

import sys
import os

sys.argv.pop( 0 )
try:
	ncores_need = int( sys.argv.pop( 0 ) )
	inode_low = int( sys.argv.pop( 0 ) )
	inode_hi = int( sys.argv.pop( 0 ) )
except:
	print "args:\tnprocs\tdiglow\tdighi\t<ignore_node1,ignore_node2,etc>\n\n\
dig[1-2] 2 hr (2 machines) \n\
dig[[3-12] 8 hrs (10 machines) \n\
dig[13-22] 24 hrs (10 machines) \n\
dig[23-26] 14days (4 machines) \n\
dig[27-34] ???? \n\
"
	sys.exit()
try:
	ignore_nodes = sys.argv.pop( 0 ).split( ',' )
except:
	ignore_nodes = []
nodename_prefix = 'dig'

ncores_node = 20
ncores_total_free = 0
ncores_free = {}
for inode in range( inode_low, inode_hi + 1 ):
	nodename = nodename_prefix + str( inode )
	if str( inode ) in ignore_nodes: continue
	#round to nearest integer
	print 'pinging', nodename, '...'
	try:
		ncores_busy = int( 0.5 + float( os.popen( 'ssh -x -o ConnectTimeout=1 ' + nodename + ' uptime' ).readline().split()[ 9 ][ :-1 ] ) )
		#skip if all cores used
		if ncores_busy >= ncores_node: continue
		#free cores cant be less than zero
		ncores_free[ nodename ] = ( ncores_node - ncores_busy )
		#go ahead and sum total free to see if we asked for too many
		ncores_total_free += ncores_free[ nodename ]
	except: continue

if ncores_total_free < ncores_need:
	print 'Not enough cores!', str( ncores_total_free ), 'cores available!'
	sys.exit()

hostfile = open( 'hostfile', 'w' )
nodefile = open( 'sshloginfile', 'w' )
ncores_taken = 0
done = False
joblist_line = 0
for nodename in sorted( ncores_free, key=lambda key: ncores_free[ key ], reverse=True ):
	ncores_grab = ncores_free[ nodename ]
	ncores_taken += ncores_grab
	#only take as many as we need
	if ncores_taken > ncores_need:
		ncores_grab -= ( ncores_taken - ncores_need )
	if ncores_taken >= ncores_need:
		done = True
	#extract ncores_grab fraction of total len joblist
	if done: break
hostfile.close()
nodefile.close()
