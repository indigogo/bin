#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tbackground_psfm\tpred_psfm\t<exp>\n"; }
$ref_psfm_filename = shift(@ARGV);
$pred_psfm_filename = shift(@ARGV);
$exp = shift(@ARGV);

@ref_psfm = `cat $ref_psfm_filename`;
chomp( @ref_psfm );
@pred_psfm = `cat $pred_psfm_filename`;
chomp( @pred_psfm );
$n_resi = 20;

# load the psfm matrices, assumes ref psfm starts before pred psfm seq length
$pred_seqpos = 0;
$ref_seqpos = 0;

foreach ( 0..$#ref_psfm ){
	@ref_freqs = split ' ', $ref_psfm[ $ref_seqpos ];
	@pred_freqs = split ' ', $pred_psfm[ $pred_seqpos ];
	$ref_pos = shift( @ref_freqs );
	$pred_pos = shift( @pred_freqs );
	if( $#ref_freqs != $n_resi - 1 ){ die "ref PSFM is not Nx20!\n"; }
	if( $ref_pos < $pred_pos ){
		++$ref_seqpos;
		next;
	}
	elsif( $pred_pos < $ref_pos ){
		++$pred_seqpos;
		next;
	}
#	if( $ref_pos > $pred_pos ){
#		if( $pred_seqpos == 0 ){ die "ref PSFM starts after pred PSFM!\n"; }
#		else{ last; }
#	}
	if( $#ref_freqs != $#pred_freqs ){ die "PSFMs are of different width at p$ref_pos!\n"; }
	++$ref_seqpos;
	++$pred_seqpos;

	print "$pred_pos\t";
	@new_freqs = 0;
	$sum = 0;
	foreach $resi( 0..$#ref_freqs ){
		if( $pred_pos == 0 ){ $new_freqs[ $resi ] = $pred_freqs[ $resi ]; }
		else{ $new_freqs[ $resi ] = $pred_freqs[ $resi ] - $ref_freqs[ $resi ]; }
		if( $new_freqs[ $resi ] < 0 ){ $new_freqs[ $resi ] = 0; }
#		elsif( $pred_freqs[ $resi ] <= $ref_freqs[ $resi ] ){ $new_freqs[ $resi ] = 0; }
#		else{ $new_freqs[ $resi ] = $pred_freqs[ $resi ]; }
		if( $exp ){ $new_freqs[ $resi ] = $new_freqs[ $resi ] ** $exp; }
		$sum += $new_freqs[ $resi ];
	}
	#renormalize to frequency
	foreach $resi( 0..$#ref_freqs ){
		if( $new_freqs[ $resi ] > 0 ){
			$new_freqs[ $resi ] = $new_freqs[ $resi ] / $sum;
			print "$new_freqs[ $resi ]\t";
		}
		else{ print "0\t"; }
	}
	print "\n";
}

