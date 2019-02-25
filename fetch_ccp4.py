#!/usr/bin/python

import sys
import os
from twill.commands import *

if( len( sys.argv ) < 2 ):
	print "args:\tpdbfile"
	sys.exit()
sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )

pdb4 = pdbname.split( '/' ).pop()[ :4 ]
pdb4 = pdb4.lower()

mapurl = 'http://eds.bmc.uu.se/cgi-bin/eds/gen_maps_zip.pl?pdbCode='+pdb4
go( mapurl )
fv( 1, 'mapformat', 'ccp4' )
submit()

ccp4url = 'http://eds.bmc.uu.se/tmp/eds/'+pdb4+'.ccp4.gz'
print ccp4url
os.system( 'wget -r -t 3 ' + ccp4url )
