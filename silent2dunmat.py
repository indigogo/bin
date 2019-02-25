#!/usr/bin/python

#################################################################

import os
import sys
import math

if( len( sys.argv ) < 2 ):
	print "args:\tsilentfile"
	print "aaidx phi psi chi1 chi2 chi3 chi4"
	sys.exit()
sys.argv.pop( 0 )
silentname = sys.argv.pop( 0 )

silentfile = open( silentname, 'r' )
silent = silentfile.readlines()

aa2idx = { 'A': 1,'C': 2,'D': 3,'E': 4,'F': 5,'G': 6,'H': 7,'I': 8,'K': 9,'L': 10,'M': 11,'N': 12,'P': 13,'Q': 14,'R': 15,'S': 16,'T': 17,'V': 18,'W': 19,'Y': 20 }

#monomers only for now
seqline = silent[ 0 ]
seqline = seqline.rstrip()
seq = seqline.split()[ 1 ]

readseq = False
#only to end - 1 to ignore term
for i in range( 1, len( silent ) - 1 ):
	#skip termini!
	parse_next = silent[ i + 1 ].split()
	if parse_next[ 0 ] == "SCORE:": continue

	line = silent[ i ]
	line = line.rstrip()
	parse = line.split()
	#if annotseq line 
	if parse[ 0 ] == "SCORE:":
		readseq = False
		continue
	if readseq:
		resi = int( parse[ 0 ] )
		#skip termini!	
		if resi == 1: continue 
		
		aa = seq[ resi - 1 ]
		aaidx = str( aa2idx[ aa ] )
		phi = parse[ 2 ]
		psi = parse[ 3 ]
		chi1 = parse[ 8 ]
		chi2 = parse[ 9 ]
		chi3 = parse[ 10 ]
		chi4 = parse[ 11 ]
		outline = [ aaidx, phi, psi, chi1, chi2, chi3, chi4 ]
		print ' '.join( outline )
	if parse[ 0 ] == "ANNOTATED_SEQUENCE:":
		readseq = True

