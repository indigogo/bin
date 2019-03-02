#!/usr/local/bin/python

import argparse
from argparse import ArgumentParser
import sys
import os
import re
import pandas as pd
import numpy as np

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument( '-pdblist', type = str, default = 'file', required = True, help = 'input pdb file list' )
	args = parser.parse_args()

	pdblistname = args.pdblist

	if pdblistname == '-':
		pdblist = sys.stdin.readlines()
	else:
		pdblist = open( pdblistname, 'r' ).readlines()

	# this dictionary holds all the dataframe data, used to init pandas dataframe
	# keys are column names, each key holds a list of col values
	d = {}

	for pdbname in pdblist:
		pdbname = pdbname.rstrip()
		pdb = open( pdbname, 'r' ).readlines()
		
		#add pdbname to dict
		pdb4 = ( pdbname.split( '/' )[ -1 ] ).split( '.' )[ -1 ]
		# init the pdb column if we havent seen it
		if not 'pdb' in d.keys():
			d[ 'pdb' ] = []
		# and add to the column
		d[ 'pdb' ].append( pdb4 )

		start_reading = False
		for line in pdb:
			# if we have seen the end of the last thing before the filter vals
			# ... check if we are there
			if not start_reading:
				start_reading = re.match( '^#END_POSE_ENERGIES_TABLE.*$', line )
				continue

			# this should match to things like 'sasa 13888.8' or 'nres 254'
			if re.match( '^\w+ -*[0-9].*$', line ):
				scoreterm = line.split()[ 0 ]
				scoreval = line.split()[ 1 ]
				# init the pdb column if we havent seen it
				if not scoreterm in d.keys():
					d[ scoreterm ] = []
				# and add to the column
				d[ scoreterm ].append( scoreval )

	# create data frame from dict
	df = pd.DataFrame( data=d )
	# write to csv
	df.to_csv( 'rs_pdb_filter_vals.csv', header='rosetta scripts output pdb filter values' )

