#!/usr/bin/perl

if( !$ARGV[ 0 ] ){ die "args:\t\n"; }
if( $ARGV[ 0 ] eq '-' ){ @ARGV = <>; }
 = shift( @ARGV ); #||

@file = `cat $filename`;
foreach $line( @file ){

}
