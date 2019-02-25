#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:\t*.byres.sc\t<wts>"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )
if len( sys.argv ) >= 1: wtsname = sys.argv.pop( 0 )
else: wtsname = False

file = open( filename, 'r' ).readlines()
#get score wts?
if wtsname:
	wts = {}
	wtsfile = open( wtsname, 'r' ).readlines()
	for wtsline in wtsfile:
		wtsparse = wtsline.split()
		#assume is name/wt value if two values on line
		if len( wtsparse ) != 2: continue
		if float( wtsparse[ 1 ] ) == 0: continue
		wts[ wtsparse[ 0 ] ] = float( wtsparse[ 1 ] )

#create dictionary for key->col
header = file.pop( 0 )
header = dict( zip( header.split(), range( len( header.split() ) ) ) )

#min/max burial vals?
#these are from yfset/nat pdb set
res_lk_burial_min = 0.174
res_lk_burial_max = 0.735
bb_lk_burial_min = 0.174
bb_lk_burial_max = 0.813
sc_lk_burial_min = 0.135
sc_lk_burial_max = 0.664

#which scores to reweight?
#terms = [ 'fa_atr', 'fa_rep', 'fa_sol', 'fa_intra_rep', 'pro_close', 'fa_pair', 'hbond_sr_bb', 'hbond_lr_bb', 'hbond_bb_sc', 'hbond_sc', 'dslf_ss_dst', 'dslf_cs_ang', 'dslf_ss_dih', 'dslf_ca_dih', 'rama', 'omega', 'fa_dun', 'p_aa_pp' ]
#res_terms = [ 'fa_atr', 'fa_rep', 'fa_sol', 'fa_pair' ]
#it probably doenst make sense to downwt clashes or fa_sol
res_terms = [ 'fa_atr', 'fa_pair' ]
bb_terms = [ 'pro_close', 'hbond_sr_bb', 'hbond_lr_bb', 'rama', 'omega', 'p_aa_pp' ]
sc_terms = [ 'hbond_bb_sc', 'hbond_sc', 'fa_dun' ]

prevname = file[ 0 ].split()[ header[ 'description' ] ]
totscore = 0
for line in file:
	parse = line.split()
	name = parse[ header[ 'description' ] ]

	#rewt from wts file
	if wtsname:
		for wtskey, wtsval in wts.iteritems():
			parse[ header[ wtskey ] ] = wtsval * float( parse[ header[ wtskey ] ] )
		
	#rescale to [0,1] with min/max values
	res_lk_burial = float( parse[ header[ 'res_lk_burial' ] ] )
	res_burial = ( res_lk_burial - res_lk_burial_min ) / ( res_lk_burial_max - res_lk_burial_min )
	res_burial = max( (res_burial, 0) )
	res_burial = min( (res_burial, 1) )
	bb_lk_burial = float( parse[ header[ 'bb_lk_burial' ] ] )
	bb_burial = ( bb_lk_burial - bb_lk_burial_min ) / ( bb_lk_burial_max - bb_lk_burial_min )
	bb_burial = max( (bb_burial, 0) )
	bb_burial = min( (bb_burial, 1) )
	sc_lk_burial = float( parse[ header[ 'sc_lk_burial' ] ] )
	sc_burial = ( sc_lk_burial - sc_lk_burial_min ) / ( sc_lk_burial_max - sc_lk_burial_min )
	sc_burial = max( (sc_burial, 0) )
	sc_burial = min( (sc_burial, 1) )

	#recalc score and wtd score, use terms in wts file?
	if wtsname:
		score = 0
		wtd_score = 0
		for wtskey in wts.keys():
			termval = parse[ header[ wtskey ] ]
			score += termval
			if wtskey in res_terms: wtd_score += res_burial * termval
			elif wtskey in bb_terms: wtd_score += bb_burial * termval
			elif wtskey in sc_terms: wtd_score += sc_burial * termval
			else: wtd_score += termval
	else:		
		#dont weight ref energy!
		score = float( parse[ header[ 'score' ] ] )
		ref = float( parse[ header[ 'ref' ] ] )
		wtd_score = ( score - ref ) * res_burial + ref

#	wtd_score = score

	out = str( totscore ) + '\t' + prevname
	#print out and reset totscore if begin of new struct
	if name != prevname:
		print out
		totscore = 0
	#if last line, add last wtd_score and print totscore
 	if line == file[ -1 ]:
		totscore += wtd_score
		print out
	else:
		#add wtd_score to totscore and reset prevname
		totscore += wtd_score		
		prevname = name
