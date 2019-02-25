#!/usr/bin/perl

if( !$ARGV[ 0 ] ){ die "args:\tfilename\n"; }
if( $ARGV[ 0 ] eq '-' ){ @ARV = <>; }
$filename = shift( @ARGV ); #||

open OUT, ">$filename.nodup";
@file = `cat $filename`;
@dups = (0)x($#file+1);
foreach $i1( 0..$#file-1 ){
	if( $dups[ $i1 ] == 1 ){ next; }
	foreach $i2( $i1+1..$#file ){
		if( $file[$i1] eq $file[$i2]){ $dups[$i2] = 1; }
	}
}
foreach $i1( 0..$#file ){
	print OUT $file[$i1] if $dups[$i1] == 0;
}
