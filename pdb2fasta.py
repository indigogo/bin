#!/usr/bin/python

## (c) Copyright Rosetta Commons Member Institutions.
## (c) This file is part of the Rosetta software suite and is made available under license.
## (c) The Rosetta software is developed by the contributing members of the Rosetta Commons.
## (c) For more information, see http://www.rosettacommons.org. Questions about this can be
## (c) addressed to University of Washington UW TechTransfer, email: license@u.washington.edu.
##
## @author: Rhiju Das
# modified to incl missing residues by Chris King

import string
from sys import argv,exit,stdout
from os import popen,system
from os.path import exists,basename

longer_names={'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
              'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
              'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
              'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
              'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

#pdbname if fasta tag, pdb is list of lines, chain or False
def pdb_to_fasta_str( pdbname, pdb, chain ):
	oldresnum = '   '
	old_chain = 'XXXXXX' #bogus chain id for init
	firstres = True
	iseq = -1
	fasta_out_str = ''
	for line in pdb:
		if not (len(line)>20): continue
		if not ( line[0:4] == 'ATOM' or (line[0:6] == 'HETATM') & (line[17:20]=='MSE') ): continue
		#skip if not correct chain
		this_chain = line[ 21 ]
		if chain and this_chain != chain: continue	
		resnum = line[23:26]
		#write new res into fasta
		if resnum != oldresnum	or this_chain != old_chain:
			iseq += 1
			#write fasta header for each chain
			if this_chain != old_chain:
				if not firstres: fasta_out_str += str( '\n' )
				fasta_out_str += str('>'+basename(pdbname) );
				fasta_out_str += str('_' + this_chain );
				fasta_out_str += str( '\n' );
				old_chain = this_chain
				firstres = False
			# add missing residues as X's
			if oldresnum != '   ':
				dresnum = int( resnum ) - int( oldresnum )
				if dresnum > 1 and add_missing:
					for ires in range( 1, dresnum ):
						fasta_out_str += str( 'X' )
						iseq += 1
			longname = line[17:20]
			if longer_names.has_key(longname):
					fasta_out_str += str( longer_names[longname] );
			else:
					fasta_out_str += str( 'X' )
		oldresnum = resnum
	fasta_out_str += str('\n')
	return fasta_out_str

if __name__ == '__main__':
	if( len( argv ) < 2 ):
					print "args:\tpdb\t<chain(-)>\t<output_dir(-(current)|STDOUT|other)>\t<add_missing(T|F)>"
					exit()
	argv.pop( 0 )
	pdbname = argv.pop( 0 )
	if len( argv ) > 0: chain = argv.pop( 0 )
	else: chain = False
	if chain == '_': chain = ' '
	if chain == '-': chain = False
	if len( argv ) > 0:
		output_dir = argv.pop( 0 )
	else: output_dir = False
	if output_dir == '-': output_dir  = False

	if len( argv ) > 0:
		add_missing = argv.pop( 0 )
		if add_missing[ 0 ].lower() == 'f': add_missing = False
		else: add_missing = True
	else: add_missing = True
	
	pdbname = pdbname
	assert( exists(pdbname))
	#print 'Reading ... '+pdbname

	#get decomp gzip from stdout, or load raw pdb
	if pdbname.split( '.' )[ -1 ] == 'gz':
		pdb = popen('gzip -c -d ' + pdbname, 'r').readlines()
		pdbname = '.'.join( pdbname.split( '.' )[ :-1 ] ) 
	else:
		pdb = open(pdbname,'r').readlines()

	if output_dir == 'STDOUT':
		fasta_out = stdout
	else:
		fastaname = '.'.join( pdbname.split( '.' )[ :-1 ] ) + '.fasta'
		if output_dir:
			if fastaname.count( '/' ): fastaname = fastaname.split( '/' )[ -1 ]
			fastaname = output_dir + '/' + fastaname
		fasta_out = open( fastaname, 'w' )

	
	#pdbname if fasta tag, pdb is list of lines, chain or False
	fasta_out_str = pdb_to_fasta_str( pdbname, pdb, chain )

	fasta_out.write( fasta_out_str )
	fasta_out.close()
