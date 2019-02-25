#!/usr/bin/python

import sys
import os
import socket
import math

gropath = '/work/bjelic/bin/GROMACS/software/bin/'
mdppath = '/work/chrisk/bin/'
restypes = [ 'ACE ', 'NH2 ', 'ALA ', 'ARG ', 'ARGN ', 'ASN ', 'ASN1', 'ASP ', 'ASPH', 'CYS ', 'CYSH', 'CYS1', 'CYS2', 'GLN ', 'GLU ', 'GLUH', 'GLY ', 'HIS ', 'HISA', 'HISB', 'HISH', 'HIS1', 'HYP ', 'ILE ', 'LEU ', 'LYS ', 'LYSH', 'MET ', 'PHE ', 'PRO ', 'SER ', 'THR ', 'TRP ', 'TYR ', 'VAL ', 'DADE', 'DGUA', 'DCYT','DTHY','ADE ','GUA ','CYT ','URA ','ZN  ','NA  ','CL  ','CA  ','MG  ','CU1 ','CU  ','H2O ','HOH ' ]

ffs = ['amber03', 'amber94', 'amber96', 'amber99', 'amber99sb', 'amber99sb-ildn', 'ambergs', 'charmm27', 'gromos43a1', 'gromos43a2', 'gromos45a3', 'gromos53a5', 'gromos53a6', 'oplsaa']

###INPUT###
if( len( sys.argv ) < 2 ):
	print "args:\tpdb_filename\ttime(ns)\t<forcfield(gromos43a1)>\t<params_filename>\t<freeze_protein(all||bb)>\t<n_threads(1)>\n\nNOTES:\nUse \'-\' for options not being used\nThe params file is optional.\nAutomated ligand parameterization only works with the default gromos43a1 forcfield!\nAuto-disulfide detection not yet supported.\nDNA molecules may or may not be converted properly.\nCurrently, gromacs_robot lets gromacs rebuild your hydrogens.\nIf you will be supplying a ligand param file, you need to add the following line to your .bashrc file:\nexport PYTHONPATH=$PATH:/work/chrisk/twill-0.9\nHere's the list of forcefields\n(if one of these ff names doesn't work, google it before asking me)\n"
	print ffs
	sys.exit()
sys.argv.pop( 0 )
pdbname = sys.argv.pop( 0 )
time = float( sys.argv.pop( 0 ) )
ff = sys.argv.pop( 0 )
if ff == '-': ff = 'gromos43a1'
#is there a ligand?
if len( sys.argv ) > 0: paramsname = sys.argv.pop( 0 )
else: paramsname = None
if paramsname == '-': paramsname = None
#restrain the protein atoms?
if( len( sys.argv ) > 0 ): freeze = sys.argv.pop( 0 )
else: freeze = False
if freeze == '-': freeze = False
if len( sys.argv ) > 0: n_threads = sys.argv.pop( 0 )
else: n_threads = 1
if n_threads == '-': n_threads = 1

name = pdbname.split( '/' ).pop()
name = '.'.join( name.split( '.' )[ :-1 ] )
#where am I?
host = socket.gethostname()
#TODO open pdbfile, then create new dir and move there
pdbfile = open( pdbname, 'r' ).readlines()
if paramsname: paramsfile = open( paramsname, 'r' ).readlines()
if not os.path.exists( name ): os.mkdir( name )
os.chdir( name )
#########

#only load twill if we need to goto the internet
if paramsname: from twill.commands import *

#######CLEAN PDB######
prot_pdbfile = open( name + '.clean.pdb', 'w' )
for line in pdbfile:
	if line[ 0:4 ] != 'ATOM' and line[ 0:3 ] != 'TER': continue
	if line[ 17:20 ] == 'CYZ': line[ 17:20 ] = 'CYS'
	if line[ 17:20 ] == 'CYD': line[ 17:20 ] = 'CYS'
	if line[ 17:20 ] == '  A': line = line[ :17 ] + 'DADE' + line[ 21: ]
	if line[ 17:20 ] == '  G': line = line[ :17 ] + 'DGUA' + line[ 21: ]
	if line[ 17:20 ] == '  C': line = line[ :17 ] + 'DCYT' + line[ 21: ]
	if line[ 17:20 ] == '  T': line = line[ :17 ] + 'DTHY' + line[ 21: ]
	if line[ 17:21 ] not in restypes: continue
	prot_pdbfile.write( line )
prot_pdbfile.close()

#get lig res name from params file
if paramsname:
	lig_resn = None
	for line in paramsfile:
		if line.split()[ 0 ] == 'NAME':
			lig_resn = line.split()[ 1 ]
			break
	#extract ligand coords from pdb
	lig_pdb = ''
	for line in pdbfile:
		if line[ 0:4 ] != 'ATOM' and line[ 0:6 ] != 'HETATM': continue
		if line[ 17:20 ] == lig_resn: lig_pdb = lig_pdb + line

	#get lig gromos params
	go( "http://davapc1.bioch.dundee.ac.uk/prodrg/submit.html" )
	fv( 1, 'coords', lig_pdb )
	fv( 1, 'clax_cha', 'WAT' )
	fv( 1, 'clax_em', '' )
	submit( 7 )
	page = show()
	coord_header = page.find( 'The GROMOS87/GROMACS coordinate file (polar/aromatic hydrogens)' )
	coord_footer = page.find( 'The GROMOS87/GROMACS coordinate file (all hydrogens)' )
	topol_header = page.find( 'The GROMACS topology' )
	topol_footer = page.find( 'The AUTODOCK 2.4 PDBQ file' )

	#TODO change charges to rosetta charges?
	lig_coords = page[ coord_header:coord_footer ].split( '\n' )[ 2:-5 ]
	lig_natoms = int( lig_coords.pop( 0 ) )
	lig_coords = '\n'.join( lig_coords )
	lig_grofile = open( lig_resn + '.gro', 'w' )
	lig_grofile.write( lig_coords )
	lig_grofile.write( '\n' )
	lig_grofile.close()

	lig_topol =  page[ topol_header:topol_footer ].split( '\n' )[ 17:-4 ]
	lig_topfile = open( lig_resn + '.itp', 'w' )
	lig_topol = '\n'.join( lig_topol )
	lig_topfile.write( lig_topol )
	lig_topfile.write( '\n' )
	lig_topfile.close()

#requires min.mdp, equil.mdp(?), md_1ns.mdp

#create .gro and .top files
#exit = os.system( gropath + 'pdb2gmx ' + '-f ' + name + '.clean.pdb -p ' + name + '.top -o ' + name + '.gro -ff ' + ff + ' -water spc -ignh  >& ' + name + '.pdb2gmx.log' )
exit = os.system( gropath + 'pdb2gmx ' + '-f ' + name + '.clean.pdb -p ' + name + '.top -o ' + name + '.gro -ff ' + ff + ' -water tip3p -ignh  >& ' + name + '.pdb2gmx.log' )
if exit == 65280: 
	print '*************\nGROMACS_ROBOT\n*************'
	print 'gromacs pdb2gmx died!\nCheck ' + name + '.pdb2gmx.log for details\ncheck that ' + name + '.clean.pdb exists and has no missing atoms!\nuse Rosetta score app to fill in missing atoms from PDB derived structures\ncheck that ' + name + '.clean.pdb has no HETATMs'
	sys.exit()

#gen position restraints for backbone only?
if freeze == 'bb':
	os.system( 'echo 4 > .' + name + '.tmp' )
	os.system( gropath + 'genrestr -f ' + name + '.gro < .' + name + '.tmp' )

#get prot coords
if paramsname:
	prot_coords = open( name + '.gro', 'r' ).readlines()
	prot_coords.pop( 0 )
	prot_natoms = int( prot_coords.pop( 0 ) )
	celldata = prot_coords.pop()
	#add lig stuff to gro and top files
	natoms = prot_natoms + lig_natoms
	grofile = open( name + '.gro', 'w' )
	grofile.write( name + '\n' )
	grofile.write( str( natoms ) + '\n' )
	grofile.writelines( prot_coords )
	grofile.write( lig_coords + '\n' )
	grofile.write( celldata )
	grofile.close()

	#get prot topol, modify, and write
	prot_topol = open( name + '.top', 'r' ).read()
	topol = prot_topol.replace( '; Include water topology', '; Inlude ligand topology\n#include \"' + lig_resn + '.itp\"\n\n; Include water topology' )
	topol = topol + lig_resn + '\t\t1\n'
	topfile = open( name + '.top', 'w' )
	topfile.write( topol )
	topfile.close()

#write the md.mdp file
tmpl_mdp = open( mdppath + 'md_1ns.mdp', 'r' ).readlines()
my_mdpfile = open( 'md.mdp', 'w' )
for mdpline in tmpl_mdp:
	if mdpline.split()[ 0 ] == 'title':
		my_mdpfile.write( mdpline )
		if freeze: my_mdpfile.write( 'define = -DPOSRES\n' )
	elif mdpline.split()[ 0 ] == 'nsteps':
		my_mdpfile.write( 'nsteps\t= ' + str( time / 2 * 1000000 ) + '\n' )
	else: my_mdpfile.write( mdpline )
my_mdpfile.close()

exit = os.system( gropath + 'editconf ' + '-f ' + name + '.gro -c -d 1.0 -bt cubic -o ' + name + '.box.gro' )
if exit == 65280: 
	print '\n*************\nGROMACS_ROBOT\n*************'
	print 'gromacs editconf died!\ncheck that ' + name + '.gro exists!'
	sys.exit()

#minimize
os.system( gropath + 'grompp ' + '-f ' + mdppath + 'min.mdp ' + '-c ' + name + '.box.gro -p ' + name + '.top -o ' + name + '.drymin.tpr' )
os.system( gropath + 'mdrun -nt ' + n_threads + ' -deffnm ' + name + '.drymin > ' + name + '.drymin.out' )
#solvate
os.system( gropath + 'genbox ' + '-cp ' + name + '.box.gro -cs spc216.gro -p ' + name + '.top -o ' + name + '.sol.gro' )
#minimize in water
os.system( gropath + 'grompp ' + '-f ' + mdppath + 'min.mdp ' + '-c ' + name + '.sol.gro -p ' + name + '.top -o ' + name + '.min.tpr' )
os.system( gropath + 'mdrun -nt ' + n_threads + ' -deffnm ' + name + '.min > ' + name + '.min.out' )
#TODO: posre solv equilibration?
#md
os.system( gropath + 'grompp ' + '-f ' + 'md.mdp ' + '-c ' + name + '.min.gro -p ' + name + '.top -o ' + name + '.md.tpr' )
os.system( gropath + 'mdrun -nt ' + n_threads + ' -deffnm ' + name + '.md >& ' + name + '.md.out' )

