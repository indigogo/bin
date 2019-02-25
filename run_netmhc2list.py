#!/usr/bin/python

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:\tfasta\tallele_list\t<peptide_mode>"
	sys.exit()
sys.argv.pop( 0 )
fastaname = sys.argv.pop( 0 )
allele_list = sys.argv.pop( 0 )
try:
	peptide_mode = sys.argv.pop( 0 )
	if peptide_mode.lower()[ 0 ] == 'f': peptide_mode = False
	else: peptide_mode = True
except:
	peptide_mode = False
	
#if cant find list, just use the string for one allele
if os.path.exists( allele_list ):
	alleles = open( allele_list, 'r' )
	allele_tag = allele_list
	if allele_tag.count( '/' ): allele_tag = allele_tag.split( '/' )[ -1 ]
	if allele_tag.count( '.' ): allele_tag = '.'.join( allele_tag.split( '.' )[ :-1 ] )
else:
	alleles = [ allele_list ]
	allele_tag = allele_list.lower()
	allele_tag = allele_tag.replace( '-', '' )
	allele_tag = allele_tag.replace( 'hla', '' )

name = '.'.join( fastaname.split( '.' )[ :-1 ] )
outname = name + '.netmhc2_' + allele_tag + '.out'
if os.path.exists( outname ): os.remove( outname )
for allele in alleles:
	allele = allele.rstrip()
	cmd = '/work/chrisk/netMHCII-2.2/netMHCII -a ' + allele + ' -f ' + fastaname 
	if peptide_mode: cmd += ' -p'
	cmd += ' >> ' + outname 
	os.system( cmd )
