#!/usr/local/bin/python

import sys
import os
from scipy.integrate import trapz

sys.argv.pop( 0 )
try:
	filename = sys.argv.pop( 0 )
	datacol = int( sys.argv.pop( 0 ) ) - 1
	classcol = int( sys.argv.pop( 0 ) ) - 1 
	n_points = int( sys.argv.pop( 0 ) )
except:
	print "args:\tfile\tdatacol\tclasscol\tn_points\t<class_cutoff>\npositives defined as above cutoff"
	sys.exit()
try:
	classcut = float( sys.argv.pop( 0 ) )
except:
	classcut = False

if filename == '-':
	file = sys.stdin.readlines()
	filename = 'data.data'
else:
	file = open( filename, 'r' ).readlines()

#read data, class vals
npos = 0
nneg = 0
datavals = []
classvals = []
for line in file:
	toks = line.rstrip().split()	
	if toks[ 0 ][ 0 ] == '#': continue
	datavals.append( float ( toks[ datacol ] ) )
	if classcut is False:
		classvals.append( bool( int( float( toks[ classcol ] ) ) ) )
	else:
		classvals.append( float( toks[ classcol ] ) <= classcut )
	if classvals[ -1 ]: npos += 1
	else: nneg += 1

assert( npos > 0 ), "no positive class found"
assert( nneg > 0 ), "no negative class found"
#iter n_points, cutoff for true/false ranges from min to max
tpr_vals = []
fpr_vals = []
deltaval = ( max( datavals ) - min( datavals ) ) / float( n_points )
for icut in range( n_points ):
	cutval = max( datavals ) - deltaval * float( icut )
	#calc false pos and true pos rates
	fp = 0
	tp = 0
	for data_class in zip( datavals, classvals ):
		#above cutoff ?
		if data_class[ 0 ] >= cutval:
			#and actually true?
			if data_class[ 1 ] is True: tp+=1
			#but actually false?
			elif data_class[ 1 ] is False: fp+=1
	tpr_vals.append( float( tp ) / float( npos ) )
	fpr_vals.append( float( fp ) / float( nneg ) )

auc = trapz( tpr_vals, x=fpr_vals )
outfilename = '.'.join( filename.split( '/' )[ -1 ].split( '.' )[ :-1 ] )
if classcut is not False: outfilename += '.cut' + str( classcut )
outfilename += '.roc'
outfile = open( outfilename, 'w' )
print outfilename + ' AUC: ' + str( auc )
for fpr, tpr in zip( fpr_vals, tpr_vals ):
	outfile.write( str( fpr ) + ' ' + str( tpr ) + '\n' )
