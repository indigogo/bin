#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tseq_file\tallele_list"
	sys.exit()
sys.argv.pop( 0 )
fastaname = sys.argv.pop( 0 )

allele_list = sys.argv.pop( 0 )
alleles = open( allele_list, 'r' )
allele_tag = allele_list
if allele_tag.count( '/' ): allele_tag = allele_tag.split( '/' )[ -1 ]
if allele_tag.count( '.' ): allele_tag = '.'.join( allele_tag.split( '.' )[ :-1 ] )

name = '.'.join( fastaname.split( '.' )[ :-1 ] )
outname = name + '.netmhc2_' + allele_tag + '.out'
if os.path.exists( outname ): os.remove( outname )
for allele in alleles:
	allele = allele.rstrip()
	# -p flag specifies"peptide mode", 1 core per fasta entry
	os.system( 'netMHCII -a ' + allele + ' -p -f ' + fastaname + ' >> ' + outname )
