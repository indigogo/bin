#!/usr/bin/perl

if( !$ARGV[ 0 ] ){ die "args:\tfilename\tn_lines||frac\n"; }

$filename = shift( @ARGV );
$n_lines = shift( @ARGV );

if( $filename eq '-' ){
	@file = <>;
}
else{
	@file = `cat $filename`;
}
$n_tot = $#file;

if( $n_lines >= 1 ){
	foreach( 1..$n_lines ){
		$line = $file[ int( rand( $n_tot ) + 1 ) ];
		print "$line";
	}
}
else{
	foreach $line( @file ){
		if( rand() < $n_lines ){ print "$line"; }
	}
}
