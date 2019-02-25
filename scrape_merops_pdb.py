#!/usr/bin/python

import sys
import os
from subprocess import call
from twill.commands import *
from gogolib import *
import re

def get_pdb_fasta_seq( pdb4, chain ):
	go( 'http://www.rcsb.org/pdb/files/fasta.txt?structureIdList=' + pdb4 )
	page = show()
	seq = ''
	reading = False
	for line in page.split( '\n' ):
		#if 1st line, get pdb chain
		if re.match( '^>\w{4}:\w.*', line ):
			this_chain = re.sub( '^>\w{4}:(\w).*', r'\1', line )
			if this_chain == chain: reading = True
			else: reading  = False
			continue
		if reading: seq += line
	return seq

def get_uniprot_pdbs( id, seqpos_begin, seqpos_end ):
	pdbs_chains = []
	go( 'http://www.uniprot.org/uniprot/' + uniprotid )
	page = show()
	if page.count( 'PDB' ):
		lines = re.split( '</tr>', page )
		for line in lines:
			toks = re.split( '[<>]', line )
			#does this line have pdb info?
			if len( toks ) < 6 or not re.search( 'a class=\"pdb\" href.*', toks[ 5 ] ): continue
			pdb4 = toks[ 6 ]
			pdb_chain = toks[ 20 ].split( '/' )[ 0 ] #gets first chain if multiple chains
			#pdb_seqpos_begin = toks[ 26 ].split( '-' )[ 0 ]
			#pdb_seqpos_end = toks[ 26 ].split( '-' )[ 1 ]
			pdbs_chains.append( [ pdb4, pdb_chain ] )
	return pdbs_chains

sys.argv.pop( 0 )
try:
	acc = sys.argv.pop( 0 )
except:
	print "args:MEROPS_acc_code(ex:C01.032)\t"
	sys.exit()

out = open( acc + '.seq', 'w' )
pdbdir = acc + '_pdbs'
if not os.path.exists( pdbdir ): os.mkdir( pdbdir )
os.chdir( pdbdir )
pdbout = open( acc + '.pdbdata', 'w' )
url = 'http://merops.sanger.ac.uk/cgi-bin/substrates?id=' + acc
go( url )
lines = show().split( '</tr>' )
for il in range( 1, len( lines ) - 1 ):
	toks = re.split( '\n+', lines[ il ] )
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
	#take uniprotID to PDB and look for structure
	uniprotid = re.split( '[<>]', toks[ 3 ] )[ 4 ]
	#skip if no ID
	if uniprotid == '': continue
	seqpos_begin = re.split( '-', re.split( '[<>]', toks[ 4 ] )[ 2 ] )[ 0 ]
	seqpos_end = re.split( '-', re.split( '[<>]', toks[ 4 ] )[ 2 ] )[ 1 ]
	#get all the PDBs assoc w/ this uniprot ID
	pdbs_chains = get_uniprot_pdbs( uniprotid, seqpos_begin, seqpos_end )
	for pdb4, pdb_chain in pdbs_chains:
		#check rcsb's fasta for desired subseq, goto next if not there
		fasta_seq = get_pdb_fasta_seq( pdb4, pdb_chain )
		if fasta_seq.find( aa1s ) < 0:  continue
		pdb4 = pdb4.lower()
		#now get the pdb, and double check that the subseq actually has coordinates in the pdb file
		call( 'getPdb.pl -id ' + pdb4, shell=True )
		call( 'gzip -df ' + pdb4 + '.pdb.Z', shell=True )
		call( 'extract_pdb_chains.py ' + pdb4 + '.pdb ' + pdb_chain + ' > ' + pdb4 + '.' + pdb_chain + '.pdb', shell=True )
		call( 'pdb2fasta.py ' + pdb4 + '.' + pdb_chain + '.pdb', shell=True )
		pdb_fasta = open( pdb4 + '.' + pdb_chain + '.fasta' ).readlines()
		[ pdb_seqs, seq_tags ] = load_fasta_seqs( pdb_fasta )
		subseq_start = pdb_seqs[ 0 ].find( aa1s )
		if subseq_start < 0: continue
		pdbout.write( ' '.join( [ aa1s, pdb4, pdb_chain, str( subseq_start + 1 ), str( subseq_start + len( aa1s ) ) ] ) + '\n' )
		#we only need one structure per protease site
		break

