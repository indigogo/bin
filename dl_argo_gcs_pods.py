#!/usr/local/bin/python

import argparse
from argparse import ArgumentParser
import sys
import os

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument( '--nametag', type = str, required = True, help = 'search string for gcs buckets defined by argo submit --name option' )
	parser.add_argument( '--project', type = str, default = 'argo-science-artifacts', required = False, help = 'gcs project name' )
	args = parser.parse_args()

	nametag = args.nametag
	project = args.project

	os.system( 'gsutil cp -r gs://' + project + '/' + nametag + '* .' )

