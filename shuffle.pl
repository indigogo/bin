#!/usr/bin/perl

if( !$ARGV[ 0 ] ){ die "args:\tfilename\tn_lines\n"; }

$filename = shift( @ARGV );
$n_lines = shift( @ARGV );

@file = `cat $filename`;
$n_tot = ( split ' ', `wc $filename` )[ 0 ]; 
foreach( 1..$n_lines ){
	$line = $file[ int( rand( $n_tot ) + 1 ) ];
	print "$line";
}
