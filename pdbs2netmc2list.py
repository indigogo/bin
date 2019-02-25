#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
try:
	pdblistname = sys.argv.pop( 0 )
	allele_list = sys.argv.pop( 0 )
except:
	print "args:\tpdblist(or '-' for stdin)\tallele_list(or name)\t<pdb_chain>"
	sys.exit()
try:
	chain = sys.argv.pop( 0 )
except:
	chain = False

if pdblistname == '-':
  pdblist = sys.stdin.readlines()
else:
  pdblist = open( pdblistname, 'r' ).readlines()

#if cant find list, just use the string for one allele
if os.path.exists( allele_list ):
	alleles = open( allele_list, 'r' ).readlines()
	allele_tag = allele_list
	if allele_tag.count( '/' ): allele_tag = allele_tag.split( '/' )[ -1 ]
	if allele_tag.count( '.' ): allele_tag = '.'.join( allele_tag.split( '.' )[ :-1 ] )
else:
	alleles = [ allele_list ]
	allele_tag = allele_list.lower()
	allele_tag = allele_tag.replace( '-', '' )
	allele_tag = allele_tag.replace( 'hla', '' )

for pdbname in pdblist:
	pdbname = pdbname.rstrip()
	if chain: os.system( 'pdb2fasta.py ' + pdbname + ' ' + chain )
	else: os.system( 'pdb2fasta.py ' + pdbname )
	name = '.'.join( pdbname.split( '.' )[ :-1 ] )
	fastaname = name + '.fasta'
	outname = name + '.netmhc2_' + allele_tag + '.out'
	if os.path.exists( outname ): os.remove( outname )
	for allele in alleles:
		allele = allele.rstrip()
		os.system( 'netMHCII -a ' + allele + ' -f ' + fastaname + ' >> ' + outname )
