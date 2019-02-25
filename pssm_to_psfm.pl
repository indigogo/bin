#!/usr/bin/perl -w
if( !$ARGV[ 0 ] ){ die "args:\tpsfm_file\tgate\n"; }
$psfm_filename = shift(@ARGV);
$gate = shift(@ARGV) || 0;

@psfm = `cat $psfm_filename`;
chomp( @psfm );
$n_resi = 20;

foreach $seqpos( 0..$#psfm ){
	@scores = split ' ', $psfm[ $seqpos ];
	$pos = shift( @scores );

	if( $#scores != $n_resi - 1 ){ die "ref PSFM is not Nx20!\n"; }

	print "$pos\t";
	$min = 99999; #sure is an ugly way to do this
	$max = -99999;
	foreach $resi( 0..$#scores ){
		#invert scores?
		if( $gate eq "neg"  ){ $scores[ $resi ] = $scores[ $resi ] * -1; }
		if( $gate && $scores[ $resi ] < 0 ){ $scores[ $resi ] = 0; }
		if( $scores[ $resi ] < $min ){ $min = $scores[ $resi ]; }
		if( $scores[ $resi ] > $max ){ $max = $scores[ $resi ]; }
	}
	#shift and stretch to [0,1]
	$sum = 0;
	foreach $resi( 0..$#scores ){
		$scores[ $resi ] = ( $scores[ $resi ] - $min );
		$sum += $scores[ $resi ];
	}
	$checksum = 0;
	foreach $resi( 0..$#scores ){
		$scores[ $resi ] = $scores[ $resi ] * 1.0 / $sum;
		$checksum += $scores[ $resi ];
		print "$scores[ $resi ]\t";
	}
	print "\n";
}

