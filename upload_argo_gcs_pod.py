#!/usr/local/bin/python

import argparse
from argparse import ArgumentParser
import sys
import os
import re

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument( '--file', type = str, required = True, help = 'file to upload' )
	parser.add_argument( '--folder', type = str, required = False, help = 'remote folder path' )
	parser.add_argument( '--project', type = str, default = 'argo-science-artifacts', required = False, help = 'gcs project name' )
	args = parser.parse_args()

	folder = args.folder
	filename = args.file
	project = args.project

	os.system( 'gsutil cp -r ' + filename + ' gs://' + project + '/' + folder + '/' + filename )
