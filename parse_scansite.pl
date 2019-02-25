#!/usr/bin/perl

if( $#ARGV < 0 ){ die "args:\tsmali_source_filename\tn_up\tn_down\n"; }
$filename = shift( @ARGV );
$nup = shift( @ARGV ) || 5;
$ndown = shift( @ARGV ) || 5;
if( $nup > 7 || $ndown > 7 ){ die "max 7 up/downstream!"; }
@file = `grep \'size="2"\' $filename`;
$name = ( split '\.', $filename )[ 0 ];
$outname = shift( @ARGV );
if( !$outname ){ $outname = $name.'.seq'; }
open SEQ, ">$outname";
foreach $line( @file ){

	$nterm = ( split '<', ( split 'size="2">', $line )[ 1 ] )[ 0 ];
	$anchor = ( split '<', ( split 'size="2"><b>', $line )[ 1 ] )[ 0 ];
	$cterm = ( split '<', ( split 'size="2">', $line )[ 3 ] )[ 0 ];

	$nterm =~ tr/* /XX/;
	$cterm =~ tr/* /XX/;

	$nterm = substr $nterm, 7 - $nup;
	$cterm = substr $cterm, 0, $ndown;

	$seq = $nterm.$anchor.$cterm;
	print SEQ "$seq\n";
}
$nterm = $nup * -1;
`gen_pssm.pl $outname psfm $nterm > $name.psfm`;
`weblogo.pl $outname 1 $nterm`;
#`gimp $name.png`;

