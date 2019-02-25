#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tfasta_sequence_filename\tpdb_template<:chain(@=wildcard):><beginres:endres>_listfile\t#_of_models\n--input files must be in working directory--\n"; }
$fasta_filename = shift( @ARGV );
$pdblist_filename = shift( @ARGV );
$n_models = shift( @ARGV );

@pdblist_file = `cat $pdblist_filename`;
chomp( @pdblist_file );
@fasta_file = `cat $fasta_filename`;
$fasta_name = ( split '\.', $fasta_filename )[ 0 ];
$seq;
foreach $line( @fasta_file ){
	chomp( $line );
	if( index( $line, '>' ) != 0 ){
		$seq = $seq.$line;
	}
}

open ALI, ">$fasta_name.ali";
print ALI ">P1;$fasta_name\nsequence\:$fasta_name\:\:\:\:\:\:\:0.00: 0.00\n$seq*\n";
close ALI;

open MALIGN, ">template.multi.aln";
print MALIGN "from modeller import *\n\n";
print MALIGN "env = environ()\n";
print MALIGN "env.io.atom_files_directory = './'\n"; 
print MALIGN "aln = alignment(env)\n";
print MALIGN "for (code, chain, first, last) in (";
foreach $line( @pdblist_file ){
	@parsed = split ':', $line;
	$pdb_filename = shift( @parsed );
	$chain = shift( @parsed ) || '@';
	$begin = shift( @parsed ) || "FIRST";
	$end = shift( @parsed ) || "LAST";
	$pdb_name = ( split '\.pdb', $pdb_filename )[ 0 ];
	print MALIGN "('$pdb_name','$chain','$begin', '$end')";
	if( $line ne $pdblist_file[ $#pdblist_file ] ){ print MALIGN ","; }
}
print MALIGN "):\n";
print MALIGN "\tmdl = model(env, file=code, model_segment=(first+':'+chain, last+':'+chain))\n";
print MALIGN "\taln.append_model(mdl, atom_files=code, align_codes=code+chain)\n\n";
print MALIGN "for (weights, write_fit, whole) in (((1., 0., 0., 0., 1., 0.), False, True),((1., 0.5, 1., 1., 1., 0.), False, True),((1., 1., 1., 1., 1., 0.), True, False)):\n";
print MALIGN "\taln.salign(rms_cutoff=3.5, normalize_pp_scores=False,rr_file='\$(LIB)/as1.sim.mat', overhang=30,gap_penalties_1d=(-450, -50),gap_penalties_3d=(0, 3), gap_gap_score=0, gap_residue_score=0,dendrogram_file='template.multi.tree',alignment_type='tree',feature_weights=weights,improve_alignment=True, fit=True, write_fit=write_fit,write_whole_pdb=whole, output='ALIGNMENT QUALITY')\n\n";
print MALIGN "aln.write(file='template.multi.pap', alignment_format='PAP')\naln.write(file='template.multi.ali', alignment_format='PIR')\n\n";
print MALIGN "aln.salign(rms_cutoff=1.0, normalize_pp_scores=False,
           rr_file='\$(LIB)/as1.sim.mat', overhang=30,
           gap_penalties_1d=(-450, -50), gap_penalties_3d=(0, 3),
           gap_gap_score=0, gap_residue_score=0, dendrogram_file='1is3A.tree',
           alignment_type='progressive', feature_weights=[0]*6,
           improve_alignment=False, fit=False, write_fit=True,
           write_whole_pdb=False, output='QUALITY')
\n";
close MALIGN;

open ALIGN, ">$fasta_name.multi.aln";
print ALIGN "from modeller import *

log.verbose()
env = environ()

env.libs.topology.read(file='\$(LIB)/top_heav.lib')

# Read aligned structure(s):
aln = alignment(env)
aln.append(file='template.multi.ali', align_codes='all')
aln_block = len(aln)

# Read aligned sequence(s):
aln.append(file='$fasta_name.ali', align_codes='$fasta_name')
# Structure sensitive variable gap penalty sequence-sequence alignment:
aln.salign(output='', max_gap_length=20,
           gap_function=True,   # to use structure-dependent gap penalty
           alignment_type='PAIRWISE', align_block=aln_block,
           feature_weights=(1., 0., 0., 0., 0., 0.), overhang=0,
           gap_penalties_1d=(-450, 0),
           gap_penalties_2d=(0.35, 1.2, 0.9, 1.2, 0.6, 8.6, 1.2, 0., 0.),
           similarity_flag=True)

aln.write(file='$fasta_name.multi.ali', alignment_format='PIR')
aln.write(file='$fasta_name.multi.pap', alignment_format='PAP')
";
close ALIGN;

open MODEL, ">$fasta_name.model.py";
print MODEL "from modeller import *\n";
print MODEL "from modeller.automodel import *\n\n";
print MODEL "env = environ()\n";
print MODEL "a = automodel(env, alnfile='$fasta_name.multi.ali', knowns = (";
foreach $line( @pdblist_file ){
	@parsed = split ':', $line;
	$pdb_filename = shift( @parsed );
	$pdb_name = ( split '\.pdb', $pdb_filename )[ 0 ];
	$chain = shift( @parsed ) || '@';
	print MODEL "'$pdb_name$chain'";
	if( $line ne $pdblist_file[ $#pdblist_file ] ){ print MODEL ", "; } 
}
print MODEL "), sequence='$fasta_name', assess_methods=(assess.DOPE))\n";
print MODEL "a.starting_model = 1\n";
print MODEL "a.ending_model = $n_models\n";
print MODEL "a.auto_align()\n";
print MODEL "a.make()\n";
close MODEL;
