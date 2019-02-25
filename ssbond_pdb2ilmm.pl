#!/usr/bin/perl

$pdbfile = shift( @ARGV );

$res1 = ( split ' ', `grep \'ATOM      1\' $pdbfile` )[ 5 ];

@ssbonds = `grep \'SSBOND\' $pdbfile`;
foreach $line( @ssbonds ){
	@parseline = split ' ', $line;
	$cys1 = $parseline[ 4 ] - $res1;
	$cys2 = $parseline[ 7 ] - $res1;
	print ", { \$$cys1.3.0, \$$cys2.3.0 }";
}
print "\n";
