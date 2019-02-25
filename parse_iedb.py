#!/usr/bin/python

#############
##############

import sys
import os

if( len( sys.argv ) < 2 ):
	print "args:csv_file\t"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )

file = open( filename, 'r' ).readlines()
#create dictionary for key->col
header_list = file.pop( 0 ).strip('\'').split(',')
#clean up the tokens
for i in range( len( header_list ) ):
	header_list[ i ] = header_list[ i ].strip()
header = dict( zip( header_list, range( len( header_list ) ) ) ) 

#get all the binding seqs sorted by allele
allele_seqs = {}
for line in file:
	line = line.split('","')
	#clean up the tokens
	for i in range( len( line ) ):
		line[ i ] = line[ i ].strip()
		line[ i ] = line[ i ].strip( '"' )

	#check for binding, skip if not Positive
	binding = line[ header[ 'Qualitative Measure' ] ]
#	binding = line[ -1 ]
	if not binding.startswith('Positive'): continue
	seq = line[ header[ 'Epitope Linear Sequence' ] ]
	#skip if empty sequence field
	if not seq: continue

	#get allele, seq
	allele = line[ header[ 'MHC Allele Name' ] ]
	allele = allele.strip()
	allele = allele.replace( ' ', '_' )
	allele = allele.replace( ',', '_' )
	allele = allele.replace( '/', '_' )
	#store seq in dict
	if not allele_seqs.has_key( allele ): allele_seqs[ allele ] = []
	#skip duplicate epitope entries!
	if seq in allele_seqs[ allele ]: continue
	allele_seqs[ allele ].append( seq )

#now print seqs to file
for allele, seqs in allele_seqs.iteritems():
	#open file for editing
	seqfile = open( os.path.splitext( filename )[ 0 ] + '.' + allele + '.fasta', 'w' )
	for iseq, seq in enumerate( seqs ):
		seqfile.write( '>seq' + str( iseq ) + '\n' )
		seqfile.write( seq + '\n' )
	seqfile.close()
