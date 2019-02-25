#!/usr/bin/perl

if( $#ARGV < 0 ){ die "args:\tsmali_source_filename\tn_up\tn_down\n"; }
$filename = shift( @ARGV );
$nup = shift( @ARGV ) || 7;
$ndown = shift( @ARGV ) || 7;
if( $nup > 7 || $ndown > 7 ){ die "max 7 up/downstream!"; }
@file = `grep \'.......<font color="red">Y</font>.......\' $filename -o | awk -F \'<|>\' \'{print \$1\$3\$5}\'`;

foreach $line( @file ){
	@seq = split( '', $line );
	foreach $pos( 0..14 ){
		if( $seq[ $pos ] eq ' ' ){ print "X"; }
		elsif( $seq[ $pos ] eq "\n" ){
			foreach( 0..14-$pos ){
				print "X";
			}
		}
		else{ print $seq[ $pos ]; }
	}
	print "\n";
}

