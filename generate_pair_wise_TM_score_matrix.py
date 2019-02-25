#!/bin/env python
import os, sys, glob,re
from os import popen, system, uname
import commands
from numpy  import *
import numpy as np

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

	#initial matrix
	tmscore=zeros( (len(pdblist),len(pdblist)) )
	for i in range(len(pdblist)):
			tmscore[i,i]=1

	for i in range(len(pdblist)):
		for j in range(i+1,len(pdblist)):
			#build filename from pdb names
			#!!WARNING HARDCODED FILENAME CONVENTION!!#
			outname = pdblist[ i ] + '_' + pdblist[ j ] + '.tmalign.out'
			tmscore[i,j]= os.popen('grep average ' + outname ).read().split()[ 1 ]

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
