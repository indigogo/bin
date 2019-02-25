#!/bin/env python
import sys
import os

def tmalign_cmd(arg):
    #print 'Parent process:', os.getppid()
    #print 'Process id:', os.getpid()
    cmd = "TMalign %s %s -a > %s_%s.tmalign.out" % (arg[0], arg[1], arg[0], arg[1])
    return cmd

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

	cmd_list=[]
	for i in range(len(pdblist)):
		for j in range(i+1,len(pdblist)):
			cmd_list.append( tmalign_cmd( [ pdblist[i],pdblist[j] ] ))

#	print cmd_list
#	print num_processes


	for cmd in cmd_list:
		print cmd

if __name__ == '__main__':
    main()
    sys.exit()
