#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tquery_tag\tClustalW_alnfile\tpdb_template<:chain(@=wildcard):><beginres:endres>_listfile\t#_of_models\n--input files must be in working directory--\n"; }
$query_tag = shift( @ARGV );
$clustal_filename = shift( @ARGV );
$pdblist_filename = shift( @ARGV );
$n_models = shift( @ARGV );

@pdblist_file = `cat $pdblist_filename`;
chomp( @pdblist_file );
@clustal_file = `cat $clustal_filename`;
$clustal_name = ( split '\.', $clustal_filename )[ 0 ];
$seq;
@query_grep = `grep -i \'$query_tag\' $clustal_filename`;
foreach $line( @query_grep ){
	$seq = $seq.( split ' ', $line )[ 1 ];
}

open ALIGN, ">$clustal_name.ali";
print ALIGN ">P1;$clustal_name\nsequence\:$clustal_name\:\:\:\:\:\:\:0.00: 0.00\n$seq*\n";

foreach $line( @pdblist_file ){
	@parsed = split ':', $line;
	$pdb_filename = shift( @parsed );
	$pdb_name = ( split '\.', $pdb_filename )[ 0 ];
	$chain = shift( @parsed ) || '@';
	$begin = shift( @parsed ) || "FIRST";
	$end = shift( @parsed ) || "LAST";
	my $seq;
	@query_grep = `grep -i \'$pdb_name\' $clustal_filename`;
	foreach $line( @query_grep ){
		$seq = $seq.( split ' ', $line )[ 1 ];
	}
	print ALIGN ">P1;$pdb_name\nstructure\:$pdb_name\:$begin\:$chain\:$end\:$chain\:\:\:0.00: 0.00\n$seq*\n";
}
close ALIGN;

open MODEL, ">$clustal_name.model.py";
print MODEL "from modeller import *\n";
print MODEL "from modeller.automodel import *\n\n";
print MODEL "env = environ()\n";
print MODEL "a = automodel(env, alnfile='$clustal_name.ali', knowns = (";
foreach $line( @pdblist_file ){
	@parsed = split ':', $line;
	$pdb_filename = shift( @parsed );
	$pdb_name = ( split '\.pdb', $pdb_filename )[ 0 ];
	print MODEL "'$pdb_name'";
	if( $line ne $pdblist_file[ $#pdblist_file ] ){ print MODEL ", "; } 
}
print MODEL "), sequence='$clustal_name', assess_methods=(assess.DOPE))\n";
print MODEL "a.starting_model = 1\n";
print MODEL "a.ending_model = $n_models\n";
print MODEL "a.make()\n";
close MODEL;
