#!/usr/bin/perl

if( $#ARGV < 0 ){ die "args:\tcommand\tlistname\n(\'=\' wildcard)\n"; }
$com = shift( @ARGV );
$list_filename = shift( @ARGV );
@list = `cat $list_filename`;
chomp( @list );

foreach( @list ){
	$this_com = $com;
	$this_com =~ s/=/$_/g;
	`$this_com`;
}
