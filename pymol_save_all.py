#!/usr/bin/python

import sys
import os
from pymol import cmd


def save_all( tag='', sel='' ):
	pdblist = cmd.get_names()
	for pdbname in pdblist:
		outname = pdbname
		if len( tag ) > 0: outname += '.' + tag
		outname += '.pdb'
		if len( sel ) > 0: pdbname += ( ' and ' + sel )
		cmd.save( outname, pdbname )

cmd.extend( 'save_all', save_all )
