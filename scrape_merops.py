#!/usr/bin/python

import sys
import os
from twill.commands import *
from gogolib import aa3_to_aa1
import re

sys.argv.pop( 0 )
try:
	acc = sys.argv.pop( 0 )
except:
	print "args:MEROPS_acc_code(ex:C01.032)\t"
	sys.exit()

url = 'http://merops.sanger.ac.uk/cgi-bin/substrates?id=' + acc
go( url )
out = open( acc + '.seq', 'w' )
lines = show().split( '</tr>' )
for il in range( 1, len( lines ) - 2 ):
	toks = lines[ il ].split( '\n' )
	if il == 1:
		itoks = range( 9, 17 )
		itype = 7
	else:
		itoks = range( 8, 16 )
		itype = 6
	#skip ncaa peptides
	peptype = re.split( '[<>]', toks[ itype ] )[ 4 ]
	if peptype == 'S': continue
	aa1s = ''
	for itok in itoks:
		aa3 = toks[ itok ].replace( '<td>', '' ).replace( '</td>', '' ).upper()
		try:
			aa1 = aa3_to_aa1[ aa3 ]
		except:
			aa1 = 'X'
		aa1s += aa1
	out.write( aa1s + '\n' )
#TODO: option to take uniprotID to PDB and look for structure
# either search pdb w/ uniprotID 
# or (better) goto http://www.uniprot.org/uniprot/[ID] and check for resrange, PDBID then goto http://pdb.org/pdb/explore/explore.do?structureId=[PDBID]
