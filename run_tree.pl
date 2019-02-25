#!/usr/bin/perl

$dirs_filename = shift( @ARGV );
@dirs = `cat $dirs_filename`;
chomp( @dirs );
$com = shift( @dirs );

$home = `pwd`;
chomp( $home );
foreach( @dirs ){
	chdir "$_";
	`$com`;
	chdir $home;
}
