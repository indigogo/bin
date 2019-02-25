#!/usr/bin/perl

$filename = shift( @ARGV );
@file = `cat $filename`;

foreach $line( @file ){
	chomp( $line );
	$entry = `grep $line data.spec`;
	print "$entry";
}
