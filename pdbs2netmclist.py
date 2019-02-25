#!/usr/bin/python

import sys
import os

sys.argv.pop( 0 )
try:
	pdblistname = sys.argv.pop( 0 )
except:
	print "args:\tpdblist(or '-' for stdin)\tallele_list(or name)"
	sys.exit()
allele_list = sys.argv.pop( 0 )

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
	os.system( 'pdb2fasta.py ' + pdbname )
	name = '.'.join( pdbname.split( '.' )[ :-1 ] )
	fastaname = name + '.fasta'
	outname = name + '.netmhc_' + allele_tag + '.out'
	if os.path.exists( outname ): os.remove( outname )
	for allele in alleles:
		allele = allele.rstrip()
		os.system( 'netMHC-3.0 -a ' + allele + ' ' + fastaname + ' >> ' + outname )
