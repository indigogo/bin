#!/usr/bin/perl
if( $#ARGV < 0 ){ die "args:\tfilename\tdelim\tstring1\t<string2>\tetc\n"; }

$filename = shift( @ARGV );
$delim = shift( @ARGV ) || ' ';
@keys = @ARGV;

@cols = ();
@header = split $delim, `grep -m 1 \'$keys[0]\' $filename`;
foreach $iheader( 0..$#header ){
	foreach $string( @keys ){
		chomp( $string );
		if( $header[ $iheader ] eq $string ){
			push( @cols, $iheader );
		}
	}
}
if( $#cols != $#keys ){ die "keys not found in header!\n"; }
#print "$col\n";
@file = `cat $filename`;
foreach $line( @file ){
	@vals = ();
	@tokens =  split $delim, $line;
	foreach $col( @cols ){
#		if( $col > $#tokens ){ die "Parsed line has too few elements at line $iline!\n"; }
		if( $col > $#tokens ){ next; }
		push( @vals, $tokens[ $col ] );
	}
	#skip the header
	if( $vals[ 0 ] eq $keys[ 0 ] ){ next; }
	foreach $val( @vals ){ print "$val\t"; }
	print "\n";
}
