#!/usr/bin/perl
if( !$ARGV[0] ){ die "args:\tfilename\tn_slices\n"; }
$filename = shift( @ARGV );
$n_slices = shift( @ARGV );

open FILE, "$filename" || die "cannot find $filename!\n";
@file = <FILE>;
$n_lines_tot = $#file + 1;
$n_lines_slice = int( $n_lines_tot / $n_slices );
$n_lines_remain = $n_lines_tot - $n_lines_slice * ( $n_slices );

@slice_lines = ( ( $n_lines_slice ) x ( $n_slices ) );
$iremain = 0;
foreach $islice( 0..$n_slices-1 ){
	if( $iremain >= $n_lines_remain ){ last; }
	$slice_lines[ $islice ] += 1;
	$iremain += 1;
}

$line = 0;
foreach $slice( 0..$n_slices-1 ){
	$slice_name_idx = $slice +1;
	$slice_filename = $filename . ".$n_slices" . ".$slice_name_idx";
	open FILE, ">$slice_filename";
	$n_lines_this = $slice_lines[ $slice ];
	foreach ( 1..$n_lines_this ){
		print FILE "$file[ $line ]";
		$line += 1;
	}
}
close FILE;
