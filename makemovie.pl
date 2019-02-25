#!/usr/bin/perl
if( !$ARGV[0] ){ die "args:\tnametag\tend\n"; }
$name = shift( @ARGV );
$end = shift( @ARGV );

foreach( 1..$end ){
	print "load $name"."$_.pdb, mov\n";
}
