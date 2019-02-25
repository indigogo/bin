#!/usr/bin/perl
if( $#ARGV < 0 ){ die "args:\tfilename\tnterm\tcterm\n"; }

$filename = shift( @ARGV );
$nterm = shift( @ARGV );
$cterm = shift( @ARGV );

@file = `cat $filename`;
foreach $pos( ( $nterm + 1 )..( $cterm - 1 ) ){	
	$phi = "p".$pos."_phi:";
	$psi = "p".$pos."_psi:";
	$phi = `ncol.pl $phi $filename`;
	$psi = `ncol.pl $psi $filename`;
	chomp( $phi );
	chomp( $psi );
	print `awk \'{print \$$phi\"\t\"\$$psi}\' $filename`;
}
