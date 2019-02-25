#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tpdb_filename_tag\toutfile\n"; }

$tag = shift( @ARGV );
$out = shift( @ARGV );

`rm $out`;
@pdbs = `ls $tag*pdb`;
foreach $ipdb( 0..$#pdbs ){
	$pdb = $pdbs[ $ipdb ];
	chomp( $pdb );
	`echo \'MODEL	$ipdb\' >> $out`;
	`cat $pdb >> $out`;
	`echo \'ENDMDL\' >> $out`;
}
