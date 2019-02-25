#!/usr/bin/perl

$file = shift( @ARGV );

@all = `grep \'!!!\' -B 1 -h $file`;

foreach( 0..$#all ){
	if( ( split ' ', $all[ $_ ] )[ 0 ] ne "!!" && ( split ' ', $all[ $_ ] )[ 0 ] ne "!!!" && ( split ' ', $all[ $_ ] )[ 0 ] ne "--" ){
		print "$all[ $_+1 ]";
	}

}
