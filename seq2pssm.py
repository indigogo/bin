#!/usr/bin/python

import sys
import os
from math import log

#single-letter AA types
restypes = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y' ]

#read command line
sys.argv.pop( 0 )
try:
	seqfilename = sys.argv.pop( 0 )
except:
	print 'args:\tseqs\t<col(1)>\t<info_wtd(f|t)>\t<log_base(2)>\t<canonical_aas_only(f|t)>'
	sys.exit()
try:
	seqcol = int( sys.argv.pop( 0 ) ) - 1
except:
	seqcol = 0
try:
	info = sys.argv.pop( 0 )
	if info.lower()[ 0 ] == 'f': info = False
except:
	info = False
try:
	logbase = float( sys.argv.pop( 0 ) )
except:
	logbase = 2.0
# only allow 20 cononical aas and output vals for all 20?
try:
	caas = sys.argv.pop( 0 )
	if caas.lower()[ 0 ] == 'f': caas = False
except:
	caas = False

nametag = seqfilename
if nametag.count( '.' ):
	nametag = '.'.join( nametag.split( '.' )[ :-1 ] )

#load pepseq output
seqs = open( seqfilename, 'r' ).readlines()

#increment matrix from sequences
freqmat = {}
nres = None
n_seqs = 0
for seq in seqs:
	#skip blank lines
	if len( seq ) < 2: continue
	#skip comments and fasta names, if fasta, must be 1seq/line!
	if seq.split()[ 0 ][ 0 ] == '>' or seq.split()[ 0 ][ 0 ] == '#': continue
	seq = seq.rstrip().split()[ seqcol ]
	if nres == None: nres = len( seq )
	#just skip if wrong seq length
	if len( seq ) != nres:
		continue
#		print 'ERROR: Sequence ' + seq + ' has wrong number elements!'
#		sys.exit()
	for iseq in range( nres ):
		aa = seq[ iseq ]

		if caas and aa not in restypes:
			print( 'letter code ' + aa + ' not in 20 canonicals!\n' )
			sys.exit()

		if not freqmat.has_key( aa ): freqmat[ aa ] = [ 0. ] * nres
		freqmat[ aa ][ iseq ] += 1.00000000000
	n_seqs += 1

#normalize by counts
for aa in sorted( freqmat.iterkeys() ):
	for iseq in range( nres ):
		freqmat[ aa ][ iseq ] = freqmat[ aa ][ iseq ] / n_seqs

#hacky, assuming len 20 alphabet
if info:
	n_aas = 20
	seqlen = len( freqmat[ 'A' ] ) #super hacky! assumes aa 'A' exists!
	#for each seqpos
	for iseq in range( seqlen ):
		#calc info content
		infosum = log( n_aas ) / log( logbase )
		for aa in freqmat.iterkeys():
			if freqmat[ aa ][ iseq ] == 0.: continue
			infosum += ( freqmat[ aa ][ iseq ] * log( freqmat[ aa ][ iseq ] ) / log( logbase ) )
		#rewt freqs by info
		for aa in freqmat.iterkeys():
			freqmat[ aa ][ iseq ] *= infosum

#print pssm
#pssmname = nametag + '.pssm'
#pssmfile = open( pssmname, 'w' )
#print data lines

if not caas:
	aas = freqmat.iterkeys()
else:
	aas = restypes

for aa in sorted( aas ):
	sys.stdout.write( aa )
	for iseq in range( nres ):
		try:
			sys.stdout.write( '\t' + '%.3f' % freqmat[ aa ][ iseq ] )
		except:
			sys.stdout.write( '\t' + '%.3f' % float( 0 ) )
	sys.stdout.write( '\n' )
#pssmfile.close()

