#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tscfile\tscoretag\tmin_wt\tdelta_wt\tmax_wts\tscoretag\tmin_wt\tdelta_wt\tmax_wt"
	sys.exit()
sys.argv.pop( 0 )
scfilename = sys.argv.pop( 0 )
#load up arg vectors for N score types to optimize
sctags = []
minwts = []
dwts = []
maxwts = []
while len( sys.argv ) > 0:
	sctags.append( sys.argv.pop( 0 ) )
	minwts.append( float( sys.argv.pop( 0 ) ) )
	dwts.append( float( sys.argv.pop( 0 ) ) )
	maxwts.append( float( sys.argv.pop( 0 ) ) )
#tmp file to be deleted at end
tmpscname = '.' + scfilename + '.rewt.tmp'

sctag1 = sctags[ 0 ]
minwt1 = minwts[ 0 ]
dwt1 = dwts[ 0 ]
maxwt1 = maxwts[ 0 ]
sctag2 = sctags[ 1 ]
minwt2 = minwts[ 1 ]
dwt2 = dwts[ 1 ]
maxwt2 = maxwts[ 1 ]

wt1 = minwt1
while wt1 <= maxwt1:
	#calc factor to subtract from current score
	modwt1 = -1.0 + wt1 #amount to subtract from scfile's implicit wt of 1.0
	wt2 = minwt2
	while wt2 <= maxwt2:
		#calc factor to subtract from current score
		modwt2 = -1.0 + wt2 #amount to subtract from scfile's implicit wt of 1.0

		# use sd.py to recalc scores and out put a new scfile
		#I hope to fucking god no one sees this disgusting piece of hack, I have groupt mtg in 2 days! lay off!
		cmd = '(echo \'rms score\'; sd.py ' + scfilename + ' - rms 1.0 score '
		cmd += str(modwt1) + ' ' + sctag1 + ' ' + str(modwt2) + ' ' + sctag2
		cmd += ') | perl -pe \'s/^/SCORE:  /\' > ' + tmpscname
		os.system( cmd )

		#get the dscore of this new scfile	
		decdisc = os.popen('decoydisc_prob.py ' + tmpscname + ' score 2.0').read().split()[-1]
		print sctag1, wt1, sctag2, wt2, decdisc

		#for the next step
		wt2 += dwt2
	wt1 += dwt1
#remove the hack tmp file, gawd this is the ugliest way of doing this
os.remove( tmpscname )
