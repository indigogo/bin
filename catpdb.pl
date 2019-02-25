#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tpdblist\tout\n"; }

$pdblist = shift( @ARGV );
$out = shift( @ARGV );
@pdbs = `cat $pdblist`;
chomp( @pdbs );
`rm $out`;

foreach $frame( 1 .. $#pdbs + 1 ){
	`echo \'MODEL	$frame\' >> $out`;
	$pdb = $pdbs[ $frame - 1 ];
	`cat $pdb >> $out`;
	`echo \'ENDMDL\' >> $out`;
}
