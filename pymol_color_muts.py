#! /usr/bin/env python

import sys
import os
from pymol import cmd

"""
author: Chris King 06/2012 (chrisk1@uw.edu)
pymol script to create selection of all residues
in 2 objects with matching chain and resid but mismatching sequence

useful for selecting designed positions
"""

def get_seq( sel ):
  sel += ' & n. ca & e. c'
  m = cmd.get_model(sel)
  seq3 = []
  chains = []
  resids = []
  for i in m.atom:
    seq3.append(i.resn)
    chains.append(i.chain)
    resids.append(i.resi)

#  seq1 = seq3_to_seq1(seq3)
  return seq3, chains, resids

def color_muts( nat_obj, dz_obj, color='magenta' ):

	nat_seq, nat_chains, nat_res = get_seq( nat_obj )
	dz_seq, dz_chains, dz_res = get_seq( dz_obj )
	n_muts = 0
#	mut_sel = '( ' + nat_obj + ' or ' + dz_obj + ' ) and ( '
	mut_sel = '( ' + dz_obj + ' ) and ( '
	for iseq in range( len( nat_seq ) ):
#		if nat_res[ iseq ] == dz_res[ iseq ] and \
#				nat_chains[ iseq ] == dz_chains[ iseq ] and \
#				nat_seq[ iseq ] != dz_seq[ iseq ] :
		#just depends on order of sequences, does not depend on pdb residue indices
		if iseq > len( dz_seq ): break
		if nat_seq[ iseq ] != dz_seq[ iseq ] :
			n_muts += 1
			#need or between each chain/res but not before first
			if n_muts > 1: mut_sel += ' or '
			mut_sel += ' chain ' + dz_chains[ iseq ] + ' and resi ' + dz_res[ iseq ] + ' '
	mut_sel += ' ) and elem c'
	cmd.color( color, mut_sel )

cmd.extend( 'color_muts', color_muts )
