#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tps_search_string\n"; }
$name = shift( @ARGV );

$me = `whoami`;
chomp( $me );
@jobs = `ps -fu $me | grep '$name' `;

foreach $job( @jobs ){
	$id =  ( split ' ', $job )[1];
	`kill $id`;
}

