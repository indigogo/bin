#!/usr/bin/perl

# file col1_tag col2_tag
if( !$ARGV[ 0 ] ){ die "args:\tfilename\tcol1_tag\tcol2_tag\n" }
$filename = shift( @ARGV );
@file = `cat $filename`;
$col1tag = shift( @ARGV );
$col2tag = shift( @ARGV );
$col1 = `ncol.pl $col1tag $filename`;
$col1--;
$col2 = `ncol.pl $col2tag $filename`;
$col2--;
foreach $line( @file ){
	@parsed = split ' ', $line;
	$sum = $parsed[ $col1 ] + $parsed[ $col2 ];
	print "$parsed[ 0 ]\t$parsed[ 1 ]\t$sum\n";
}
