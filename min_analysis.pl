#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tfilename\tlast_scoretype\n"; }
$file = shift( @ARGV );
$scoretype = shift( @ARGV );

@line = split ' ', `head $file -n 1`;
$ncol = $#line + 1;

$col1 = `ncol.pl $scoretype\_score: $file` + 2;

for( $col = $col1; $col <= $ncol; $col+=2 ){
	$sortcol = $col - 1;
	@line = split ' ', `sort -rn +$sortcol $file | tail -n 1`;
	$min = $line[ $sortcol ];
	$label = $line[ $sortcol - 1 ];
	print "$label\t$min\n";
}
