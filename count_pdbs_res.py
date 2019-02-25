#!/usr/bin/python

from sys import argv,exit
from os import popen,system
from os.path import exists,basename

if( len( argv ) < 2 ):
        print "args:\tpdblist\t<chain>"
        exit()
argv.pop( 0 )
pdblistname = argv.pop( 0 )
if len( argv ) > 0: chain = argv.pop( 0 )
else: chain = False

pdblist = open(pdblistname,'r').readlines()
for pdbname in pdblist:
	pdbname = pdbname.strip()
	assert( exists(pdbname))
	#print 'Reading ... '+pdbname

	#get decomp gzip from stdout, or load raw pdb
	if pdbname.split( '.' )[ -1 ] == 'gz':
		pdb = popen('gzip -c -d ' + pdbname, 'r').readlines()
		pdbname = '.'.join( pdbname.split( '.' )[ :-1 ] ) 
	else:
		pdb = open(pdbname,'r').readlines()

	if chain == '_': chain = ' '
	oldresnum = '   '
	old_chain = 'XXXXXX' #bogus chain id for init
	firstres = True
	iseq = 0
	for line in pdb:
		if (len(line)>20):
			if line[0:4] == 'ATOM' or (line[0:6] == 'HETATM') & (line[17:20]=='MSE'):
				#skip if not correct chain
				this_chain = line[ 21 ]
				if chain and this_chain != chain: continue	
				resnum = line[23:26]
				#write new res into fasta
				if resnum != oldresnum	or this_chain != old_chain:
					iseq += 1
					oldresnum = resnum
					old_chain = this_chain
	print pdbname, str( iseq )
