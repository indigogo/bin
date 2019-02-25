#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\ttag\tstart\tend\toutfile\n"; }

$tag = shift( @ARGV );
$start = shift( @ARGV );
$n = shift( @ARGV );
$out = shift( @ARGV );

`rm $out`;
foreach $frame( $start..$n ){
	$pdb = $tag.".".$frame.".pdb";
	`echo \'MODEL	$frame\' >> $out`;
	`cat $pdb >> $out`;
	`echo \'ENDMDL\' >> $out`;
}
