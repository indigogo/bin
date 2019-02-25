#!/usr/bin/python

import sys
import os

#make a copy of the template pdb with only the graft loop(s) and the target
#graft loop must be last in template... let's automate this
def write_graft_tmpl_pdb_and_count_nres( pdbname, graft_chain, graft_seqpos_begin, graft_seqpos_end, out_name ):
	pdb = open( pdbname, 'r' ).readlines()
	tmpl_pdb = open( out_name, 'w' )
	target_pdb = []
	graft_pdb = []
	nres_target = 0
	for line in pdb:
		#skip comments/ hetatms, ters, and alt atom locations
		if line[ 0:4 ] != 'ATOM': continue
		if line[ 16 ] != ' ' and line[ 16 ] != 'A': continue
		#add to target pdb and skip if wrong chain 
		if line[ 21 ] != graft_chain:
			target_pdb.append( line )
			#sum up residue count for each CA
			#TODO: this is could miscount if any nonprot or missing CA line in target's pdb lines
			if line[ 12:16 ].strip() == 'CA':
				nres_target += 1
			continue
		#skip if outside range on template pdb
		if int( line[ 22:26 ].strip() ) < graft_seqpos_begin or int( line[ 22:26 ].strip() ) > graft_seqpos_end: continue
		#add to graft pdb if in bounds 
		graft_pdb.append( line )
	#make sure we found the graft loop
	#TODO: actually count residues and make sure is right length
#	if len( graft_pdb ) != ( graft_seqpos_end - graft_seqpos_begin + 1 ):
	if len( graft_pdb ) < 1:
		print 'ERROR: graft chain, res range not found in native pdb!'
		sys.exit()
	tmpl_pdb.writelines( target_pdb )
	tmpl_pdb.writelines( graft_pdb )
	tmpl_pdb.close()
	return nres_target

#write the necessary input (paths.txt and ranges) files for multigraft to this directory
#uses location of scaffold set and length of target in tmpl pdb
def write_multigraft_input_files( graft_seqpos_begin, graft_seqpos_end, rosetta_db_path ):
	paths = open( 'paths.txt', 'w' )
	paths.write( \
			'Rosetta Input/Output Paths (order essential) \n' + \
			'path is first /, ./,or  ../ to next whitespace, must end with / \n' + \
			'INPUT PATHS: \n' + \
			'pdb1                            ./ \n' + \
			'pdb2                            ./ \n' + \
			'alternate data files            ./ \n' + \
			'fragments                       ./ \n' + \
			'structure dssp,ssa (dat,jones)  ./ \n' + \
			'sequence fasta,dat,jones        ./ \n' + \
			'constraints                     ./ \n' + \
			'starting structure              / \n' + \
			'data files                      ' + rosetta_db_path + '/\n' + \
			'OUTPUT PATHS: \n' + \
			'movie                           ./ \n' + \
			'pdb path                        ./ \n' + \
			'score                           ./ \n' + \
			'status                          ./ \n' + \
			'user                            ./ \n' + \
			'FRAGMENTS: (use ***** in place of pdb name and chain) \n' + \
			'2                                      number of valid fragment files \n' + \
			'3                                      frag file 1 size \n' + \
			'aa*****03_05.200_v1_3                               name \n' + \
			'9                                      frag file 2 size \n' + \
			'aa*****09_05.200_v1_3                               name \n' \
	)
	paths.close()
	#now ranges file, TODO: option for multiple grafts
	ranges = open( 'ranges', 'w' )
	ranges.write( \
			'loop: 1 \n' + \
			'full_range: ' + str( graft_seqpos_begin ) + ' ' + str( graft_seqpos_end ) + '\n' + \
			'nranges: 1  \n' + \
			'range: ' + str( graft_seqpos_begin ) + ' ' + str( graft_seqpos_end ) + '\n\n' \
	)

#run rough_match
def run_rough_match( tmpl_pdbname, nres_target, scaffold_pdblistname, out_name, rosetta_path ):
	os.system( rosetta_path + '  \
			-paths paths.txt  \
			-loop_ranges ranges  \
			-epi_graft -match  \
			-rough_match  \
			-input_file ' + scaffold_pdblistname + '\
			-output_file ' + out_name + '  \
			-native_complex ' + tmpl_pdbname + ' \
			-nres_Ab ' + str( nres_target ) + ' \
			-E_align  \
			-S_align  \
			-fluidize_takeoff  \
			-max_closure_rms 1.5  \
			-fluidize_landing  \
			-compute_cbeta_neighbors  \
			-rough_match_closure_rms 1.5  \
			-max_intra_clash 3000  \
			-max_inter_clash 10000  \
			-termini_residue_skip 4 >& rough_match.log \
	')

#filter rough match
#  awk '{if(($28 < 1.5) && ($29 < 0.75) && ($30 < 0.75) ) print $1" "$2" " $3" "$4" "$5" "$6" "$7" $ graft_bb graft_sc @ ....|.*.|...."}' $1
#TODO: allow cmdline option for defining filter cutoffs
def run_filter_rough_match( tmpl_pdbname, nres_target, rough_match_out_name, out_name, cut_rms_overall, cut_rms_term, cut_intra_clash, cut_inter_clash ):
	rough_match_out = open( rough_match_out_name, 'r' ).readlines()
	rough_match_out_filt = open( out_name, 'w' )
	ncol_rms_overall = 27
	ncol_rms_nterm = 28
	ncol_rms_cterm = 29
	ncol_intra_clash = 31
	ncol_inter_clash = 32
#	cut_intra_clash = 50.
#	cut_inter_clash = 1000.
	for line in rough_match_out:
		line = line.strip().split()
		#skip header/comments
		if line[ 0 ][ 0 ] == '#': continue
		if float( line[ ncol_rms_overall ] ) < cut_rms_overall and \
				float( line[ ncol_rms_nterm ] ) < cut_rms_term and \
				float( line[ ncol_rms_cterm ] ) < cut_rms_term and \
				float( line[ ncol_intra_clash ] ) < cut_intra_clash and \
				float( line[ ncol_inter_clash ] ) < cut_inter_clash:
			for ncol in range( 0, 8 ):
				rough_match_out_filt.write( line[ ncol ] + ' ' )
			rough_match_out_filt.write( ' $ graft_bb graft_sc @ ....|.*.|....\n' )
	rough_match_out_filt.close()

#run multigraft
def run_multigraft( tmpl_pdbname, nres_target, rough_match_filt_out_name, out_name, rosetta_path ):
	os.system( rosetta_path + '  \
			-paths paths.txt \
			-loop_ranges ranges \
			-epi_graft -multigraft \
			-input_file ' + rough_match_filt_out_name + ' \
			-output_file ' + out_name + '  \
			-native_complex ' + tmpl_pdbname + ' \
			-nres_Ab ' + str( nres_target ) + ' \
			-use_non_monotone_line_search -ex1 -ex1aro -ex2 -extrachi_cutoff 5 \
			-atom_vdw_set highres \
			-close_as_ALA -grow_as_ALA \
			-graft_with_Ab \
			-repack_Ab \
			-build_loops -refine_loops \
			-refine_with_constraints \
			-design_after_closure \
			-refine_with_Ab_after_design \
			-closure_attempts 10 \
			-store_n_best_closures 3 \
			-design_attempts 2 \
			-store_n_best_designs 1 \
			-max_chainbreak_score 0.2 \
			-design_after_closure \
			-compute_cbeta_neighbors >& multigraft.out \
	')


sys.argv.pop( 0 )
try:
	native_pdbname = sys.argv.pop( 0 )
	graft_chain = sys.argv.pop( 0 )
	graft_seqpos_begin = int( sys.argv.pop( 0 ) )
	graft_seqpos_end = int( sys.argv.pop( 0 ) )
	scaffold_pdblistname = sys.argv.pop( 0 )
except:
	print 'args:\tnative_pdb\tgraft_chain\tgraft_seqpos_begin\tgraft_seqpos_end\tscaffold_list\t<overall_rms_cutoff(1.5)>\t<termini_rms_cutoff(0.75)\t<intra_clash_cutoff(500)>\t<inter_clash_cutoff(2000)>\t<restart_from_rough_filter(False)>\t<rosetta++_path>\t<rosetta++_db_path>'
	print 'Notes:\n\t- scaffold list must include full file paths!\n\t- only single continuous grafts currently supported'
	sys.exit()
#and optional args
try:
	cut_rms_overall = float( sys.argv.pop( 0 ) )
except:
	cut_rms_overall = 1.5
try:
	cut_rms_term = float( sys.argv.pop( 0 ) )
except:
	cut_rms_term = 0.75
try:
	cut_intra_clash = sys.argv.pop( 0 )
	if cut_intra_clash == 'None': cut_intra_clash = 99999999
	else: cut_intra_clash = float( cut_intra_clash )
except:
	cut_intra_clash = 500
try:
	cut_inter_clash = sys.argv.pop( 0 )
	if cut_inter_clash == 'None': cut_inter_clash = 99999999
	else: cut_inter_clash = float( cut_inter_clash )
except:
	cut_inter_clash = 2000
try:
	refilter = sys.argv.pop( 0 )
	if refilter == 'false' or refilter == 'False' or refilter == 'F' or refilter == 'f' or refilter == 'FALSE':
		refilter = False
except:
	refilter = False
try:
	rosetta_path = sys.argv.pop( 0 )
except:
	rosetta_path = '/work/strauch/bin/rosetta.intel'
if not os.path.exists( rosetta_path ):
		print 'ERROR: executable', rosetta_path, 'not found!'
		sys.exit()
try:
	rosetta_db_path = sys.argv.pop( 0 )
except:
	rosetta_db_path = '/scratch/ROSETTA/rosetta_database/'
if not os.path.exists( rosetta_db_path ):
		print 'ERROR: directory', rosetta_db_path, 'not found!'
		sys.exit()

#TODO: add gzip functionality
if native_pdbname[ -4: ] != '.pdb':
	print 'ERROR: native_pdbname must in in ".pdb" extension!'
	sys.exit()

#check that scaffold pdbs in set have full path
scaffold_pdblist = open( scaffold_pdblistname, 'r' ).readlines()
for scaffold_pdbname in scaffold_pdblist:
	#skip comments
	if scaffold_pdbname[ 0 ] == '#': continue
	if scaffold_pdbname[ 0 ] != '/':
		print 'ERROR: scaffold pdblist must include full paths! entry', scaffold_pdbname, 'does not start with "/"'
		sys.exit()
	#only check the first entry (for fastness in long lists)
	else: break

#get nametags for unique output filenames, necessary in case someone runs multiple instances of graftbot in same directory
native_nametag = native_pdbname.replace( '.pdb', '' )
if native_nametag.count( '/' ) > 0: native_nametag = native_nametag.split( '/' )[ -1 ]
scaffold_nametag = scaffold_pdblistname
if scaffold_nametag.count( '/' ) > 0: scaffold_nametag = scaffold_nametag.split( '/' )[ -1 ]
#get output names
tmpl_pdbname = native_nametag + '.graft.pdb'
rough_match_out_name = native_nametag + '.' + scaffold_nametag + '.rough_match.out'
rough_match_filt_out_name = native_nametag + '.' + scaffold_nametag + '.rough_match.filtered.out'
multigraft_out_name = native_nametag + '.' + scaffold_nametag + '.multigraft.out'

#create graft template pdb from native pdb and graft loop range, also calc number res in target
print 'cleaning native pdb and writing graft template pdb...',
nres_target = write_graft_tmpl_pdb_and_count_nres( native_pdbname, graft_chain, graft_seqpos_begin, graft_seqpos_end, tmpl_pdbname )
print tmpl_pdbname, 'created,', str( nres_target ), 'residues identified in target'
if nres_target < 1:
	print 'ERROR: no CA atoms found in target coords! Cannot count number residues!'
	sys.exit()

#and some other files
#TODO give common matching path to paths.txt and mod pdblist so is not super long dir structure for output
write_multigraft_input_files( graft_seqpos_begin, graft_seqpos_end, rosetta_db_path )

#skip rerunning rough match if we're rerunning graftbot after a rough match filter fail
if not refilter:
	#need to get rid of previous rough_match run output, otherwise will append to output with duplicate entries
	if os.path.exists( rough_match_out_name ):
		print 'previous rough matching output found, deleting...'
		os.remove( rough_match_out_name )
	#run rough match
	print 'running rough matching on scaffold set...',
	run_rough_match( tmpl_pdbname, nres_target, scaffold_pdblistname, rough_match_out_name, rosetta_path )
	#and make sure it ran
	if not os.path.exists( rough_match_out_name ):
		print 'ERROR: rough_match multigraft produced no output! check rough_match.log for errors...'
		sys.exit()
	rough_match_out = open( rough_match_out_name, 'r' ).readlines()
	if len( rough_match_out ) < 1:
		print 'ERROR: rough_match found no matches! try new scaffolds or adjust rosetta options in this script'
		sys.exit()
	print 'found', len( rough_match_out ), 'matches in', scaffold_pdblistname

#filter rough match for low rmsd to graft
print 'filtering rough matches...',
run_filter_rough_match( tmpl_pdbname, nres_target, rough_match_out_name, rough_match_filt_out_name, cut_rms_overall, cut_rms_term, cut_intra_clash, cut_inter_clash )
rough_match_filt_out = open( rough_match_filt_out_name, 'r' ).readlines()
if len( rough_match_filt_out ) < 1:
	print 'ERROR: rough_match filtering eliminated all matches! try new scaffolds or'
	print 'adjust filter cutoffs in this script and rerun with "restart_from_rough_filter" option'
	sys.exit()
print len( rough_match_filt_out ), 'matches remain'

#run full multigraft design on entries that passed filter
print 'running multigraft design...'
run_multigraft( tmpl_pdbname, nres_target, rough_match_filt_out_name, multigraft_out_name, rosetta_path )

