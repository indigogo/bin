#!/usr/bin/perl
if( !$ARGV[0] ){ die "args:\tfilename\tn_dices\n"; }
$filename = shift( @ARGV );
$n_dices = shift( @ARGV );

open FILE, "$filename" || die "cannot find $filename!\n";
@file = <FILE>;

$dice_name_idx = 0;
while ( $#file >= 0 ){
	$dice_name_idx += 1;
	$dice_filename = $filename . ".$dice_name_idx";
	open FILE, ">$dice_filename";
	foreach $i( 1..$n_dices ){
		$out = shift( @file );
		print FILE $out;
		if( $#file < 0 ){
			last;
		}
	}
}
close FILE;
