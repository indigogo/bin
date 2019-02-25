#!/usr/bin/perl

$outname = "data.out";
@outfile = `cat $outname`;
$specname = shift( @ARGV );
@specfile = `cat $specname`;
@avg = ( ( 0 ) x 257 );
@n = ( ( 0 ) x 257 );

foreach $specline( @specfile ){
	$score = ( split ' ', $specline )[ 2 ];
	$pdbname = ( split '_1\.pdb', $specline )[ 0 ];
	foreach $outline( @outfile ){
		$testname = ( split ' ', $outline )[ 1 ];
		if( $testname eq $pdbname ){
			$init = ( split '/', ( split ' ', $outline )[ 3 ] )[ 5 ];
			$initindex = ( split '\.', ( split '_', $init )[ 1 ] )[ 0 ];
			$avg[ $initindex ] += $score;
			$n[ $initindex ] += 1;
#			print "$initindex\t$score\n";
		}
	}
}
foreach $i( 1..$#avg ){
	$count = $n[ $i ];
	if( $count == 0 ){ $score = 0; }
	else{ $score = $avg[ $i ] / $n[ $i ]; }
	print "$i\t$score\t$count\n";
}
