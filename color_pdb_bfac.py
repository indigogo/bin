#!/usr/bin/python
## Authors: Mike Tyka
## Authors: Chris King

import sys
import string

if len( sys.argv ) < 2:
    print sys.argv[0]+' pdbfile  tagfile'
    print
    sys.exit()


if len(sys.argv) < 3:
    Help()

pdbfile = sys.argv[1]
tagfile = sys.argv[2]

data = open(tagfile,'r').read()
lines = string.split(data,'\n')
tags = []
bfacs = []
for i in lines:
	token = string.split(i)
	if len(token) < 2 : continue;
	bfac = float(token[1])
	tags.append( [ int( float(token[0]) ),  bfac ] )
	bfacs.append( bfac )
min_bfac  = min( bfacs )
max_bfac  = max( bfacs )
	

#shift and scale range to [0,99.99]
for i,j in enumerate(tags):
	tags[i][1] = ( j[1] - min_bfac ) * 99.99 / ( max_bfac - min_bfac )


data = open(pdbfile,'r').read()
lines = string.split(data,'\n')
for i in lines:
	token = string.split(i)
	if len(token) < 6 : continue;
	if token[0] == "ATOM":
		res = int( i[22:26] )
		## find residue number
		temp = 0.0
		for j in tags:
		  if int(j[0]) == int(res):
				temp = j[1]

		temps = "% 4.2f"%float(temp);
		i = i[0:61] + temps + i[66:]

	print i









