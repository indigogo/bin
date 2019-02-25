#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )

file = open( filename, 'r' )

aas = [ 'ALA', 'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN', 'PRO', 'GLN', 'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR' ]
nres = { 'ALA': 0,'CYS': 0,'ASP': 0,'GLU': 0,'PHE': 0,'GLY': 0,'HIS': 0,'ILE': 0,'LYS': 0,'LEU': 0,'MET': 0,'ASN': 0,'PRO': 0,'GLN': 0,'ARG': 0,'SER': 0,'THR': 0,'VAL': 0,'TRP': 0,'TYR': 0 }


for line in file:
	for aa in aas:
		if line.find( aa ) != -1:
			nres[ aa ] += 1
for aa in aas:
	print nres[ aa ], 

