
import sys
import os
from pymol import cmd

#make it pretty

pdblist = cmd.get_names()
pdbid_curr = 'foo'
res_chain = 'foo'
res_chain_last = 'bar'
for i_pdb in range( len( pdblist ) ):
	cmd.hide( 'ev' )
	pdb = pdblist[ i_pdb ]
	pdbparse = pdb.split( '.' )

	#hide everything w/ diff pdbID
	pdbid = pdbparse[ 0 ]
	if len( pdbparse ) <= 3:
		cmd.color( 'green', pdb + ' and elem c' )
	cmd.color( 'cyan', pdbid + '* and (resn a or resn c or resn g or resn t or resn da or resn dt or resn dg or resn dc) and elem c' )
	
	#make it pretty
	cmd.show( 'nb_spheres', pdbid + '* and resn hoh' )
	cmd.show( 'lines', pdbid + '* and not elem h' )
	cmd.show( 'ribbon', pdbid + '*' )

	#parse filename, get resid, zoom, store scene
	if len( pdbparse ) > 2:
		pdbid_curr = pdbid
		res_chain = pdbparse[ -1 ]	
		if pdbid_curr != pdbid or res_chain != res_chain_last:
			if res_chain.find( '_' ) > -1:
				res = res_chain.split( '_' )[ 0 ]	
				chain = res_chain.split( '_' )[ 1 ]
				cmd.show( 'sticks', pdbid + '* and resi ' + res + ' and chain ' + chain + ' and not elem h' )
				cmd.orient( pdb + ' and resi ' + res + ' and chain ' + chain )
			else:
				res = res_chain
				cmd.show( 'sticks', pdbid + '* and resi ' + res + ' and not elem h' )
				cmd.orient( pdb + ' and resi ' + res )
			cmd.scene( 'new', 'store', '', 1, 1 )	
			res_chain_last = res_chain
	
	pdbid_last = pdbid

#cmd.extend("color_by_attype",color_by_attype)
