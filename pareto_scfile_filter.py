#!/usr/bin/python

import sys
import os

longer_names={'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
              'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
              'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
              'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
              'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

#pdbname if fasta tag, pdb is list of lines, chain or False
def pdb_to_fasta_str( pdbname, pdb, chain ):
  oldresnum = '   '
  old_chain = 'XXXXXX' #bogus chain id for init
  firstres = True
  iseq = -1
  fasta_out_str = ''
  for line in pdb:
    if not (len(line)>20): continue
    if not ( line[0:4] == 'ATOM' or (line[0:6] == 'HETATM') & (line[17:20]=='MSE') ): continue
    #skip if not correct chain
    this_chain = line[ 21 ]
    if chain and this_chain != chain: continue  
    resnum = line[23:26]
    #write new res into fasta
    if resnum != oldresnum  or this_chain != old_chain:
      iseq += 1
      #write fasta header for each chain
      if this_chain != old_chain:
        if not firstres: fasta_out_str += str( '\n' )
        fasta_out_str += str('>'+os.path.basename(pdbname) );
        fasta_out_str += str('_' + this_chain );
        fasta_out_str += str( '\n' );
        old_chain = this_chain
        firstres = False
      # add missing residues as -'s
      if oldresnum != '   ':
        dresnum = int( resnum ) - int( oldresnum )
        if dresnum > 1:
          for ires in range( 1, dresnum ):
            fasta_out_str += str( '-' )
#            fasta_out_str += str( 'X' )
            iseq += 1
      longname = line[17:20]
      if longer_names.has_key(longname):
          fasta_out_str += str( longer_names[longname] );
      else:
          fasta_out_str += str( 'X' )
    oldresnum = resnum
  fasta_out_str += str('\n')
  return fasta_out_str

"""

# get min/max for each dimension
# return dict of [ min, max ]
def calc_min_max( coords ):
	minmax = {}
	# calc min, max
	for icoord, coord in enumerate( coords ):
		for key in sorted( coord.iterkeys() ):
			val = coord[ key ]
			# init from first occurence?
			if not minmax.has_key( key ):
				minmax[ key ] = [ val, val ]
			# else update [ min, max ]
			else:
				minmax[ key ][ 0 ] = min( val, minmax[ key ][ 0 ] )
				minmax[ key ][ 1 ] = max( val, minmax[ key ][ 1 ] )
	return( minmax )

# takes a list of dicts of filter name->vals, one per structure, and a dict of filtername->cutoff
# returns a boolean list of is_pareto? from coords
def is_nth_percentile( coords, filterfracs ):

	# get min/max for each dimension
	filterminmax = calc_min_max( coords )

	# calc absolute cutoff associated with nth percentile
	filterfrac_cuts = {}
	for key in sorted( filterfracs.iterkeys() ):
		# cutoff = fraction * ( max - min ) + min
		filterfrac_cuts[ key ] = ( filterfracs[ key ] * ( minmax[ key ][ 1 ] - minmax[ key ][ 0 ] ) + minmax[ key ][ 0 ] )

	# loop over each coord to check if any dim is outside percentile cutoff
	for icoord, coord in enumerate( coords ):
		# set default this_is_pctile True (so we keep it)
		this_is_pctile = True
		for key in sorted( coord.iterkeys() ):
			val = coord[ key ]
		# loop over each dimension
			# if is outside cutoff, set this_is_pctile False and break
		# append this_is_pctile to is_pctile
	
	#return T/F vector
#	return is_pctile

"""

# takes a list of dicts of filter name->vals, one per structure
# returns a boolean list of is_pareto? from coords
def calc_pareto_front( coords ):
	is_pfront = []
	# enumerate over coordinates and calc whether each is dominated in all-by-all 
	for icoord, coord in enumerate( coords ):
		# check whether this coord is domainated
		is_dom = False
		for iother_coord, other_coord in enumerate( coords ):
			if icoord == iother_coord: continue
			is_dom = True
			is_equal = True
			for key in sorted( coord.iterkeys() ):
				is_equal = is_equal and ( coord[ key ] == other_coord[ key ] )
				#coord not dominated if less in any dimension (minimizing)
				if not coord.has_key( key ): 
					print "ERROR: Wrong number of columns at this row! no data for key " + key
					print icoord, coord
					sys.exit()
				if not other_coord.has_key( key ): 
					print "ERROR: Wrong number of columns at this row! no data for key " + key
					print iother_coord, other_coord
					sys.exit()
				if coord[ key ] < other_coord[ key ]:
					is_dom = False
					break
			if is_equal: 
				is_dom = False
			if is_dom:
				break
		# assign bool value to truth list
		if is_dom:
			is_pfront.append( False )
		else:
			is_pfront.append( True )
	#return T/F vector
	return is_pfront

## returns a list of filter name->values
def pdblist_to_scfile( pdblist, filtertypes ):
	scores = []
	#generate scfile header string from filtertypes list
	header = 'SCORE:\t' + '\t'.join( sorted( filtertypes.iterkeys() ) ) + '\tdescription\n'
	scores.append( header )
	#gewt scorefile style strings for each pdb file
	for pdbname in pdblist:
		pdbname = pdbname.rstrip()
		pdb = open( pdbname, 'r' ).readlines()
		#load each pdb
		start_reading = False
		filter_vals = {}
		for line in pdb:
			line = line.rstrip().split()
			if len( line ) < 1:
				continue
			#load each filter value
			#WARNING! assumes filter vals listed after #END_POSE_ENERGIES_TABLE tag in pdb
			if line[ 0 ] == '#END_POSE_ENERGIES_TABLE':
				start_reading = True

			#if this looks like a filter val line, add it or init dict
			if start_reading and len( line ) == 2:
				try:
					tag = line[ 0 ]
					val = line[ 1 ]
					#skip if not in filter types list
					if len( filtertypes ) > 0 and ( tag not in filtertypes.iterkeys() ):
						continue
					filter_vals[ tag ] = val
				except:
					continue
		#check that all filter sets are identical by checking with filtertypes
		if not sorted( filter_vals.iterkeys() ) == sorted( filtertypes.iterkeys() ):
			print "WARNING: inconsistent filter types in file " + pdbname
			[ sys.stdout.write( key + ', ' ) for key in sorted( filter_vals.iterkeys() ) ]
			sys.exit()
		#now generate scorefile-style space delim line
		score = 'SCORE:\t'
		for filter_key in sorted( filtertypes.iterkeys() ):
			score += ( filter_vals[ filter_key ] + '\t' )
		#add description column w pdb name
		if pdbname.count( '.' ) > 0:
			description = '.'.join( pdbname.split( '.' )[ :-1 ] )
		else:
			description = pdbname
		score += ( description + '\n' )
		scores.append( score )
	return scores

# takes a list of scfile lines
# returns a list of dicts of column_name --> val
def load_scfile_filtered_vals( header, scores, filtertypes, filtercuts ):
	coords = []
	scores_fltrd = []
	for line_str in scores:
		line = line_str.rstrip().split()
		coord = {}
		skip_line = False
		for ival, val in enumerate( line ):
			#try to store as a number, else skip
			try:
				val = float( val )
			except:
				continue
			#skip if not in filter types list
			if len( filtertypes ) > 0 and ( header[ ival ] not in filtertypes.iterkeys() ):
				continue
			#take negative if want to maximize instead of minimize
			if len( filtertypes ) > 0:
				#skip if not above/below filter cutoff
				if( filtercuts[ header[ ival ] ] != None and 
						filtertypes[ header[ ival ] ] == 'high' and 
						val < filtercuts[ header[ ival ] ] ):
					skip_line = True
					break
				elif( filtercuts[ header[ ival ] ] != None and 
						filtertypes[ header[ ival ] ] == 'low' and 
						val > filtercuts[ header[ ival ] ] ):
					skip_line = True
					break
				#take negative if want to maximize instead of minimize
				if( filtertypes[ header[ ival ] ] == 'high' ):
					val = -1 * val
			coord[ header[ ival ] ] = val
		if skip_line == True:
			continue
		#add current sc line and parsed pareto space coordinate to return lists
		scores_fltrd.append( line_str )
		coords.append( coord )
	return [ scores_fltrd, coords ]

#returns T/F if 2 seqs do/dont match within a tolerance of n
def is_seq_match( seq1, seq2, tol ):
	n_muts = 0
	for iaa in range( min( len( seq1 ), len( seq2 ) ) ):
		if seq1[ iaa ] != seq2[ iaa ]:
			n_muts += 1
	if n_muts > tol:
		return False
	else:
		return True

#get sequence of structure from sequence header if exists, else extract from pdb listed in 'description'
#concatenates multichain sequences!
def get_scline_pdb_sequence( scline, chain_id ):
	seq = ''
	pdbname = scline.rstrip().split()[ header_cols[ 'description' ] ] + '.pdb'
	if os.path.exists( pdbname ):
		#fasta = os.popen( '/work/chrisk/bin/pdb2fasta.py ' + pdbname + ' - STDOUT' )
		pdb = open( pdbname, 'r' ).readlines()
		fasta = pdb_to_fasta_str( pdbname, pdb, chain_id ).split( '\n' )[ :-1 ]
		seq = ''.join( [ l.strip() if l[ 0 ] != '>' else '' for l in fasta ] )
	else:
		print 'WARNING! Could not find pdb ' + pdbname
	return seq

# returns T/F and sequence str if line's sequence is in bank of best_scores' sequences
def is_seq_redundant( line_seq, best_scores, seq_match_tol, header_cols, chain_id ):
	is_redundant = False
	#load seq from scfile, else get from pdb
	for best_scline in best_scores:
		#load seq from scfile, else get from pdb
		try:
			best_scline_seq = best_scline.rstrip().split()[ header_cols[ 'sequence' ] ]
		except:
			best_scline_seq = get_scline_pdb_sequence( best_scline, chain_id )
		is_redundant = is_redundant or is_seq_match( line_seq, best_scline_seq, seq_match_tol )
		if is_redundant:
			return is_redundant
	return is_redundant

#### BEGIN ####
sys.argv.pop( 0 )
try:
	scfilename = sys.argv.pop( 0 )
	filterlist  = open( sys.argv.pop( 0 ), 'r' ).readlines()
	n_out = int( sys.argv.pop( 0 ) )
except:
	print "args:\tscfile_or_pdblist(-)\t<filter_types>\tnum_output\t<seq_tol(-1)>\t<chain_id>\t<ignore_seq(false)>\nfilter_types sets high/low optimization and cutoffs e.g.\nfilter_name high 2.5\nother_name low -10.0\tsimilar sequences eliminated if <have seq_tol> or fewer diffs"
	sys.exit()
try:
	seq_match_tol = int( sys.argv.pop( 0 ) )
except:
	seq_match_tol = -1
try:
	chain_id = sys.argv.pop( 0 )
except:
	chain_id = False
try:
	ignore_seq = sys.argv.pop( 0 )
	if ignore_seq.lower()[ 0 ] == 'f':
		ignore_seq = False
	elif ignore_seq.lower()[ 0 ] == 't':
		ignore_seq = True
except:
	ignore_seq = False

#load filterlist
# optionally load filter cutoffs
filtertypes = {}
filtercuts = {}
for line in filterlist:
	line = line.rstrip().split()
	if line[ 0 ][ 0 ] == '#': continue
	filtertypes[ line[ 0 ] ] = line[ 1 ]
	if len( line ) > 2:
		filtercuts[ line[ 0 ] ] = float( line[ 2 ] )
	else:
		filtercuts[ line[ 0 ] ] = None

# read or generate input scfile
if scfilename == '-':
	scfile = sys.stdin.readlines()
else:
	scfile = open( scfilename, 'r' ).readlines()
#scfile is actually a pdblist?
if scfile[ 0 ].rstrip().split( '.' )[ -1 ] == 'pdb':
	scfile = pdblist_to_scfile( scfile, filtertypes )
	#print scfile

# load or generate header labels
header = scfile[ 0 ].rstrip().split()
while header[ 0 ] != 'SCORE:' and len( scfile ) > 0:
	del scfile[ 0 ]
	header = scfile[ 0 ].rstrip().split()
header_cols = dict( zip( header, range( len( header ) ) ) )
#add sequence column if not already in there, unless we're ignoring sequence
if not ignore_seq and 'sequence' not in header:
	header.append( 'sequence' )
	header_cols[ 'sequence' ] = len( header ) - 1
scores = scfile[ 1: ]
best_scores = []

#scores gets smaller w/ each iteration as lines moved into best_scores
while len( scores ) > 0:
	#init list of filter vals for each pdb, each element is dict of filter name -> val
	[ scores, coords ] = load_scfile_filtered_vals( header, scores, filtertypes, filtercuts )
	is_pfront = calc_pareto_front( coords )
	assert( len( is_pfront ) == len( scores ) )
	remain_scores = []
	#accumulate best (current pareto) scores into best
	for iline, line in enumerate( scores ):
		#if is pareto, add line to best_scores unless it is seq reduntant w current best
		if is_pfront[ iline ]:
			#check current sc line seq for redundancy, skip if matches any in best
			#get sequence, add it to current line if necessary
			if not ignore_seq:
				try:
					line_seq = line.rstrip().split()[ header_cols[ 'sequence' ] ]
				except:
					line_seq = get_scline_pdb_sequence( line, chain_id )
					line = line.rstrip() + '\t' + line_seq + '\n'
				#skip this check is seq tol is zero
				if seq_match_tol > -1:
					if is_seq_redundant( line_seq, best_scores, seq_match_tol, header_cols, chain_id ):
						continue
			#else add it to best cache
			best_scores.append( line )
			#bail if we've reached our max # best limit
			if len( best_scores ) >= n_out:
				break
		else:
			remain_scores.append( line )
	if len( best_scores ) >= n_out:
		break
	scores = remain_scores

# sort final output by total_score if it is in filter types
if 'total_score' in filtertypes.keys():
	best_scores.sort( key = lambda x: float( x.split()[ header_cols[ 'total_score' ] ] ) )

[ sys.stdout.write( tok + ' ' ) for tok in header ]
sys.stdout.write( '\n' )
for iline, line in enumerate( best_scores ):
		print line.rstrip(),
		sys.stdout.write( '\n' )

