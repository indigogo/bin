#!/usr/bin/perl
if( $#ARGV < 0 ){ die "args:\tstring\tfilename\t<delim>\n"; }

$string = shift( @ARGV );
$filename = shift( @ARGV );
$delim = shift( @ARGV ) || '/\s/';

@line = split $delim, `grep -m 1 \'$string\' $filename`;
foreach( 0..$#line ){
	if( $line[ $_ ] eq $string ){
		$col = $_ ;
		print "$col\n";
	}
}

