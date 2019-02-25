#!/bin/env python
import os, sys, glob,re
from os import popen, system, uname
import commands
import multiprocessing
import subprocess
from numpy  import *
from multiprocessing import Pool
import numpy as np

def tmalign(arg):
    #print 'Parent process:', os.getppid()
    #print 'Process id:', os.getpid()
    cmd = [ "/work/krypton/bin/TMalign %s %s -a | grep average" % (arg[0], arg[1]) ]
    print "running " + cmd[ 0 ]
    return float(subprocess.check_output(cmd, shell=True).split()[1])

def main():
	#load all pdbs
	filelst=[]
	for arg in sys.argv:
        	filelst.append(arg)
	del filelst[0]


	pdblist=[]
	for fname in filelst:
        	if os.path.isfile(fname):
                	pdblist.append(fname)
 	#for file in glob.glob("*.pdb"):
    	#	pdblist.append(file)

	#initial matrix
	tmscore=zeros( (len(pdblist),len(pdblist)) )
	for i in range(len(pdblist)):
			tmscore[i,i]=1

	num_processes = multiprocessing.cpu_count() - int( round( float(popen("uptime | sed -e 's|\,||g' | awk {'print $(NF-2), $(NF-1), $NF'}").readline().split()[0]), 0 ))

	myPool    = Pool( processes = num_processes )
	
	cmd_list=[]
	for i in range(len(pdblist)):
		for j in range(i+1,len(pdblist)):
			cmd_list.append((pdblist[i],pdblist[j]))

#	print cmd_list
#	print num_processes

	myResults = myPool.map_async( tmalign, cmd_list )

	results = myResults.get()

	for i in range(len(pdblist)):
		for j in range(i+1,len(pdblist)):
			tmscore[i,j]=results.pop(0)

	#assign the other half
	for i in range(len(pdblist)):
		for j in range(i+1,len(pdblist)):
			tmscore[j,i]=tmscore[i,j]

	#print matrix
	np.savetxt("TM_score_matrix.txt",tmscore)

	f = open ("pdblist.txt", "w")
	f.writelines( list( "%s\n" % item for item in pdblist ) )
	f.close()

if __name__ == '__main__':
    main()
    sys.exit()
