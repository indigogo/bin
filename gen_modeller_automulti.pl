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

open ALIGN, ">$fasta_name.aln";
print ALIGN ">P1;$fasta_name\nsequence\:$fasta_name\:\:\:\:\:\:\:0.00: 0.00\n$seq*\n";

foreach $line( @pdblist_file ){
	@parsed = split ':', $line;
	$pdb_filename = shift( @parsed );
	$chain = shift( @parsed ) || '@';
#	$type = shift( @parsed );
	$begin = shift( @parsed ) || "FIRST";
	$end = shift( @parsed ) || "LAST";
	$pdb_name = ( split '\.pdb', $pdb_filename )[ 0 ];
#	print ALIGN ">P1;$pdb_name\nstructure$type\:$pdb_name\:$begin\:$chain\:$end\:$chain\:\:\:0.00: 0.00\n$seq*\n";
	print ALIGN ">P1;$pdb_name\nstructure\:$pdb_name\:$begin\:$chain\:$end\:$chain\:\:\:0.00: 0.00\n*\n";
}
close ALIGN;

open MODEL, ">$fasta_name.model.py";
print MODEL "from modeller import *\n";
print MODEL "from modeller.automodel import *\n\n";
print MODEL "env = environ()\n";
print MODEL "a = automodel(env, alnfile='$fasta_name.aln', knowns = (";
foreach $line( @pdblist_file ){
	@parsed = split ':', $line;
	$pdb_filename = shift( @parsed );
	$pdb_name = ( split '\.pdb', $pdb_filename )[ 0 ];
	print MODEL "'$pdb_name'";
	if( $line ne $pdblist_file[ $#pdblist_file ] ){ print MODEL ", "; } 
}
print MODEL "), sequence='$fasta_name', assess_methods=(assess.DOPE))\n";
print MODEL "a.starting_model = 1\n";
print MODEL "a.ending_model = $n_models\n";
print MODEL "a.auto_align()\n";
print MODEL "a.make()\n";
close MODEL;
