#!/usr/bin/perl
if( $#ARGV < 0 ){ die "args:\tstring\tfilename\n"; }

$string = shift( @ARGV );
$filename = shift( @ARGV );

@line = split ' ', `grep -m 1 \'$string\' $filename`;
foreach( 0..$#line ){
	if( $line[ $_ ] eq $string ){
		$col = $_ + 2;
		print "$col\n";
	}
}

