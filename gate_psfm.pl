#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tbackground_psfm\tcutoff\n"; }
$ref_psfm_filename = shift(@ARGV);
$cut = shift(@ARGV);

@ref_psfm = `cat $ref_psfm_filename`;
chomp( @ref_psfm );
$n_resi = 20;

# load the psfm matrices, assumes ref psfm starts before pred psfm seq length
$pred_seqpos = 0;

foreach ( 0..$#ref_psfm ){
	@ref_freqs = split ' ', $ref_psfm[ $_ ];
	$ref_pos = shift( @ref_freqs );

	print "$ref_pos\t";
	$sum = 0;
	foreach $resi( 0..$#ref_freqs ){
		if( $ref_freqs[ $resi ] < $cut ){ $ref_freqs[ $resi ] = 0; }
		#$ref_freqs[ $resi ] = $ref_freqs[ $resi ]**$exp;
		$sum += $ref_freqs[ $resi ];
	}
	#renormalize to frequency
	foreach $resi( 0..$#ref_freqs ){
		if( $ref_freqs[ $resi ] > 0 ){
			$ref_freqs[ $resi ] = $ref_freqs[ $resi ] / $sum;
			print "$ref_freqs[ $resi ]\t";
		}
		else{ print "0\t"; }
	}
	print "\n";
}

