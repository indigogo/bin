#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\tscfile\tscoretag\tmin_wt\tdelta_wt\tmax_wt"
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


def recurse( sctags, minwts, dwts, maxwts, modcmd ):
	sctag = sctags.pop()
	minwt = minwts.pop()
	dwt = dwts.pop()
	maxwt = maxwts.pop()

	etc etc
	
	wt = minwt
	while wt <= maxwt:
		#calc factor to subtract from current score
		modwt = -1.0 + wt #amount to subtract from scfile's implicit wt of 1.0

		# use sd.py to recalc scores and out put a new scfile
		#I hope to fucking god no one sees this disgusting piece of hack, I have groupt mtg in 2 days! lay off!
		cmd = '(echo \'rms score\'; sd.py all.semiex_split.sc - rms 1.0 score ' + str(modwt) + ' ' + sctag + ') | perl -pe \'s/^/SCORE:  /\' > ' + tmpscname
		modcmd += ' ' + str(modwt) + ' ' + sctag + ' '
		cmd += modcmd
		cmd += ') | perl -pe \'s/^/SCORE:  /\' > ' + tmpscname
		os.system( cmd )

		if len( sctags ) > 0: recurse()
		else
		#get the dscore of this new scfile	
		decdisc = os.popen('decoydisc_prob.py ' + tmpscname + ' score 1.5').read().split()[-1]
		print wt, decdisc

		#for the next step
		wt += dwt






for itag in range( len( sctags ) ):
	sctag = sctags[ itag ]
	minwt = minwts[ itag ]
	dwt = dwts[ itag ]
	maxwt = maxwts[ itag ]

	wt = minwt
	while wt <= maxwt:
		#calc factor to subtract from current score
		modwt = -1.0 + wt #amount to subtract from scfile's implicit wt of 1.0

		# use sd.py to recalc scores and out put a new scfile
		#I hope to fucking god no one sees this disgusting piece of hack, I have groupt mtg in 2 days! lay off!
		cmd = '(echo \'rms score\'; sd.py all.semiex_split.sc - rms 1.0 score ' + str(modwt) + ' ' + sctag + ') | perl -pe \'s/^/SCORE:  /\' > ' + tmpscname
		modcmd += ' ' + str(modwt) + ' ' + sctag + ' '
		cmd += modcmd
		cmd += ') | perl -pe \'s/^/SCORE:  /\' > ' + tmpscname
		os.system( cmd )

		#get the dscore of this new scfile	
		decdisc = os.popen('decoydisc_prob.py ' + tmpscname + ' score 1.5').read().split()[-1]
		print wt, decdisc

		#for the next step
		wt += dwt

