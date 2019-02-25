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
$max = 0;

@pwm = ();
$n = 0;
$max = 0;
@sums = ();
$nterm = 99999999999;

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
	if( $pred_pos < $nterm ){ $nterm = $pred_pos; }
#	if( $ref_pos > $pred_pos ){
#		if( $pred_seqpos == 0 ){ die "ref PSFM starts after pred PSFM!\n"; }
#		else{ last; }
#	}
	if( $#ref_freqs != $#pred_freqs ){ die "PSFMs are of different width at p$ref_pos!\n"; }
	++$ref_seqpos;
	++$pred_seqpos;

	@new_freqs = 0;
	$sum = 0;
	foreach $resi( 0..$#ref_freqs ){
		if( $pred_pos == 0 ){ $new_freqs[ $resi ] = $pred_freqs[ $resi ]; }
		else{
			$pred_freqs[ $resi ] += 0.05;
			$ref_freqs[ $resi ] += 0.05;
			$new_freqs[ $resi ] =  log( $pred_freqs[ $resi ] / $ref_freqs[ $resi ] );
		}
		if( $new_freqs[ $resi ] < 0 ){ $new_freqs[ $resi ] = 0; }
		if( $exp ){ $new_freqs[ $resi ] = $new_freqs[ $resi ] ** $exp; }
		$sum += $new_freqs[ $resi ];

		$pwm[ $n ] = $pwm[ $n ]."$new_freqs[ $resi ]\t";
	}
	if( $sum > $max ){ $max = $sum; }
	$sums[ $n ] = $sum;
	++$n;
}

foreach $n( 0..$#pwm ){
	@new_freqs = split ' ', $pwm[ $n ];
	$fill = $max - $sums[ $n ];
	$split = $fill / 20.0;
	$pos = $nterm + $n;
	print "$pos\t";
	foreach $f( @new_freqs ){
		if( $pos != 0 ){ $f = ( $f + $split ) / $max; }
		print "$f\t";
	}
	print "\n";
}





	#renormalize to frequency
#	foreach $resi( 0..$#ref_freqs ){
#		if( $new_freqs[ $resi ] > 0 ){
#			$new_freqs[ $resi ] = $new_freqs[ $resi ] / $sum;
#			print "$new_freqs[ $resi ]\t";
#		}
#		else{ print "0\t"; }
#	}
#	print "\n";

