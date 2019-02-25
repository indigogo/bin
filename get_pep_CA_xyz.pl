#!/usr/bin/perl

if( !$ARGV[0] ){ die "args:\tpdblist\tpep_chain\n"; }
$filename = shift( @ARGV );
$pep_chain = shift( @ARGV );

@file = `cat $filename`;
foreach $line( @file ){
	$pdbname = ( split ' ', $line )[ 0 ];
	@pdb = `grep \' $pep_chain \' $pdbname | grep \' CA \'`;
	print "$pdbname\t";
	foreach $ca( @pdb ){
		@pdbline = split ' ', $ca;
		$x = $pdbline[ 6 ];
		$y = $pdbline[ 7 ];
		$z = $pdbline[ 8 ];
		print "$x\t$y\t$z\t";
	}
	print "\n";
}
