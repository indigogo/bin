#!/usr/bin/python

import sys
import os
import math

if( len( sys.argv ) < 2 ):
	print "args:dxfile\t<filter?True||(False)>\t<lowcut(0.9)>\t<hicut(1.1)>"
	sys.exit()
sys.argv.pop( 0 )
filename = sys.argv.pop( 0 )

filter = False
lowcut = 0.9
hicut = 1.1
if len( sys.argv ) > 0: filter = bool( sys.argv.pop( 0 ) )
if len( sys.argv ) > 0: lowcut = float( sys.argv.pop( 0 ) )
if len( sys.argv ) > 0: hicut = float( sys.argv.pop( 0 ) )

file = open( filename, 'r' ).readlines()
#get nelements
parse = file.pop( 0 ).split()
nx = parse[ 5 ]
ny = parse[ 6 ]
nz = parse[ 7 ]

#get origin 
parse = file.pop( 0 ).split()
x0 = parse[ 1 ]
y0 = parse[ 2 ]
z0 = parse[ 3 ]

#get stepsize
parse = file.pop( 0 ).split()
dx = parse[ 1 ]
parse = file.pop( 0 ).split()
dy = parse[ 2 ]
parse = file.pop( 0 ).split()
dz = parse[ 3 ]

file.pop( 0 )
parse = file.pop( 0 ).split()
ntot = parse[ 9 ]

#now get data
i = -1
ifilter = -1
maxres = 9999
maxatm = 99999
chains = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz"
maxchain = len( chains )
while len( file ) > 1:
	parse = file.pop( 0 ).split()
	for val in parse:
		i += 1
		val = float( val )

		#skip if b/t lowcut and hicut?
		if filter and ( val >= lowcut and val <= hicut ) : continue
		#each output index is consecutive
		ifilter += 1

		#calc coord, loop with moduli
		iz = i  % int( nz )
		z = float( z0 ) + iz * float( dz )
		iy = int( ( i / int( nz ) ) % int( ny ) )
		y = float( y0 ) + iy * float( dy )
		ix = int( ( i / ( int( ny ) * int( nz ) ) ) % int( nx ) )
		x = float( x0 ) + ix * float( dx )
		#need to conserve indices so we dont run out of space in pdb cols
		#loop res, then chains, then atoms in res if necessary
		ires = ifilter % maxres + 1
		ichain = int( ifilter / maxres ) % maxchain
		iatm = int( ifilter / ( maxres * maxchain ) ) % maxatm + 1

		#print pdb line
		pdb = "HETATM"
		pdb += "%5d" % iatm
		pdb += "  O   "
		pdb += "HOH"
		pdb += " " 
		pdb += chains[ ichain ]
		pdb += "%4d" % ires
		pdb += "    "
		pdb += "%8.3f" % x
		pdb += "%8.3f" % y
		pdb += "%8.3f" % z
		pdb += "%6.2f" % 1.0
		pdb += "%6.2f" % val
		print pdb
#		print str( x ), str( y ), str( z ), val


