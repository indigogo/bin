#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tpsfm_file\n"; }
$psfm_filename = shift(@ARGV);

@psfm = `cat $psfm_filename`;
chomp( @psfm );
$n_resi = 20;
$n_elements = 20 * $#psfm;
$log_2 = log(2);
$log_2_of20 = log(20) / $log_2;

foreach $seqpos( 0..$#psfm ){
	@scores = split ' ', $psfm[ $seqpos ];
	$pos = shift( @scores );

	if( $#scores != $n_resi - 1 ){ die "ref PSFM is not Nx20!\n"; }

	print "$pos\t";
	$info_sum = $log_2_of20;
	foreach $resi( 0..$#scores ){
		if( $scores[ $resi ] > 0 ){ $info_sum += $scores[ $resi ] * log( $scores[ $resi ] ) / $log_2 };
	}
	foreach $resi( 0..$#scores ){
		$scores[ $resi ] = $scores[ $resi ] * $info_sum;
		print "$scores[ $resi ]\t";
	}
	print "\n";
}

