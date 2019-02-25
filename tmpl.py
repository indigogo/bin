#!/usr/local/bin/python

import argparse
from argparse import ArgumentParser
import sys
import os
import re

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument( '-file', type = str, default = 'file', required = True, help = 'input file' )
	parser.add_argument( '-option', type = str, default = 'a', choices = [ 'a', 'b', 'c' ], help = 'option' )
	parser.add_argument( '-options', type = str, nargs = '+', help = 'options list' )
	args = parser.parse_args()

	filename = args.file

	if filename == '-':
		file = sys.stdin.readlines()
	else:
		file = open( filename, 'r' ).readlines()

	for line in file:
		toks = line.rstrip().split()
