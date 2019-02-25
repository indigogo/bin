#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tref_psfm\tpred_psfm\t<dream>\ngive '-' for ref_psfm to get info content"; }

$ref_psfm_filename = shift(@ARGV);

$pred_psfm_filename = shift(@ARGV);
@pred_psfm = `cat $pred_psfm_filename`;
chomp( @pred_psfm );

$pred_nterm = ( split ' ', $pred_psfm[ 0 ] )[ 0 ];

$dream = shift(@ARGV);

if( $ref_psfm_filename eq '-' ){
	$out = &get_total_info( \@pred_psfm );
#	print "$out";
}
else{

	@ref_psfm = `cat $ref_psfm_filename`;
	chomp( @ref_psfm );
	$n_resi = 20;
	$n_elements = 20 * $#pred_psfm;

	$log_2_of_20 = log( 20 ) / log( 2 );

# load the psfm matrices, assumes ref psfm starts before pred psfm seq length
	$pred_seqpos = 0;
	$ref_seqpos = 0;
	$js = 0;
	$dist = 0;
	$dist_wtd = 0;
	$H_wtd = 0;
	$rank = 0;
	$eucl_dist = 0;

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

		if( $pred_pos == 0 ){ next; }

		if( $dream eq 'dream' ){
			$eucl_dist += &nth_eucl_dist( \@ref_freqs, \@pred_freqs, 2 );
		}
		else{
			$ref_info = $log_2_of_20 - &H( \@ref_freqs, \@ref_freqs );
			$pred_info = $log_2_of_20 - &H( \@pred_freqs, \@pred_freqs );
			$lambda = 0.9;

			$js_this = &lambda_div( \@ref_freqs, \@pred_freqs, $lambda );
			$js += $js_this;
			$rank_this = &rank_score( \@ref_freqs, \@pred_freqs );
			$rank += $rank_this;
			$dist_this = &nth_eucl_dist( \@ref_freqs, \@pred_freqs, 2 );
			$dist += $dist_this;
			$H_wtd_this = $lambda * $ref_info + ( 1.0 - $lambda ) * $pred_info;
			$dist_wtd_this = $dist_this * $H_wtd_this;
			$H_wtd += $H_wtd_this;
			$dist_wtd += $dist_wtd_this;
		}
#	print "$pred_pos\t$dist_wtd_this\n";
	}

$normscore = $dist_wtd / $H_wtd;
printf "%.3f\n", $normscore;

#normalize by n positions
#$js_norm = $js / $pred_seqpos; 
#printf "%.3f %.3f\n", $js, $js_wtd;
#print js, js_norm
#printf "%.3f bits $pred_seqpos positions\n", $js;
#printf "%.3f points $pred_seqpos positions\n", $dist;
#	if( $dream eq 'dream' ){ printf "%.3f dist %.3f maxdist $pred_seqpos positions\n", sqrt( $eucl_dist ), sqrt( $pred_seqpos ); }
#	else{ printf "%.3f bits %.3f maxbits $pred_seqpos positions\n", $dist_wtd, $H_wtd; }
#printf "%.3f points $pred_seqpos positions\n", $rank;

}

sub nth_eucl_dist{
	my @k = @{ shift( @_ ) };
	my @l = @{ shift( @_ ) };
	my $exp = shift( @_ );

	my $dist = 0;
	foreach $resi( 0..$#k ){
		$dist += ( abs( $k[ $resi ] - $l[ $resi ] ) ** $exp );
	}
	return $dist;
}

sub wtd_avg_prof{
	my @j = @{ shift( @_ ) };
	my @s = @{ shift( @_ ) };
	my $wt = shift( @_ );

	my @avg = 0;
	foreach $resi( 0..$#j ){
		$avg[ $resi ] = ( $wt * $j[ $resi ] ) + ( ( 1 - $wt ) * $s[ $resi ] );
	}
	return \@avg;
}

sub avg_prof{
	my @j = @{ shift( @_ ) };
	my @s = @{ shift( @_ ) };

	my @avg = 0;
	foreach $resi( 0..$#j ){
		$avg[ $resi ] = 0.5 * ( $j[ $resi ] + $s[ $resi ] );
	}
	return \@avg;
}

sub kl_div{
	my @k = @{ shift( @_ ) };
	my @l = @{ shift( @_ ) };

	return ( &H( \@k, \@l ) - &H( \@k, \@k ) );
}

sub lambda_div{
	my @j = @{ shift( @_ ) };
	my @s = @{ shift( @_ ) };
	my $wt = shift( @_ );

	my @avg = @{ &wtd_avg_prof( \@j, \@s, $wt ) };
	return ( $wt * &kl_div( \@j, \@avg ) + ( 1 - $wt ) * &kl_div( \@s, \@avg ) );
}

sub js_div{
	my @j = @{ shift( @_ ) };
	my @s = @{ shift( @_ ) };

	my @avg = @{ &avg_prof( \@j, \@s ) };
	return 0.5 * ( &H( \@j, \@avg ) - &H( \@j, \@j ) + &H( \@s, \@avg ) - &H( \@s, \@s ) );
}

sub H{
	my @k = @{ shift( @_ ) };
	my @l = @{ shift( @_ ) };

	my $H = 0;
	foreach $resi( 0..$#k ){
		if( $k[ $resi ] == 0 ){ next; }
		$H += $k[ $resi ] * &log2( $l[ $resi ] );
	}
	return -$H;
}

sub log2{
	my $n = shift( @_ );
	return log( $n )/log( 2 );
}

sub rank_prof{
	my @p = @{ shift( @_ ) };
	my %phash;
	my @rank;
	foreach $i( 0..$#p ){
		$phash{ $i } = $p[ $i ];
	}
	my @map = sort { $phash{ $b } cmp $phash{ $a } } keys %phash;
	foreach $i( 0..$#map ){
		$rank[ $map[ $i ] ] = $i;
	}
	return @rank;
}

sub get_total_info{
	my @p = @{ shift( @_ ) };
	$info = 0;
	foreach ( 0..$#p ){
		@p_freqs = split ' ', $p[ $_ ];
		shift( @p_freqs );
		$H = ( $log_2_of_20 - &H( \@p_freqs, \@p_freqs ) );
		$info += $H;
		$this_pos = $_ + $pred_nterm;
		print "$this_pos\t$H\n";
	}
	$max = $#p * 4.32;
#	return "$info bits $max maxbits $#p positions\n";
}

sub rank_score{
	my @p = @{ shift( @_ ) };
	my @q = @{ shift( @_ ) };

#get n zeros in p, q
	my $p_zeros = 0;
	my $q_zeros = 0;
	foreach $i( 0..$#p ){
		if( $p[ $i ] == 0.0 ){ ++$p_zeros; }
		if( $q[ $i ] == 0.0 ){ ++$q_zeros; }
	}
	my @p_rank = &rank_prof( \@p );
	my @q_rank = &rank_prof( \@q );
	my $p_info = $log_2_of_20 - &H( \@p, \@p );
	my $q_info = $log_2_of_20 - &H( \@q, \@q );
	my $refwt = 0.9;

	my $rank_score = 0;
	foreach $i( 0..$#p_rank ){
#if one prob is zero, incr. rank up to highest zero but not past other 
		if( $p[ $i ] == 0.0 && $q[ $i ] > 0.0 ){ $p_rank[ $i ] = &max( ( 19 - $p_zeros / 2 ), $q_rank[ $i ] ); }
		if( $q[ $i ] == 0.0 && $p[ $i ] > 0.0 ){ $q_rank[ $i ] = &max( ( 19 - $q_zeros / 2 ), $p_rank[ $i ] ); }
		if( $p[ $i ] == 0.0 && $q[ $i ] == 0.0 ){ $p_rank[ $i ] = $q_rank[ $i ]; }

		my $rank_diff = abs( $p_rank[ $i ] - $q_rank[ $i ] );
#		my $wt = $refwt * $p[ $i ] + ( 1 - $refwt ) * $q[ $i ];
		my $wt = $refwt * $p[ $i ] ** 2 + ( 1 - $refwt ) * $q[ $i ] ** 2;
#		my $wt =( $refwt * ( $p_rank[ $i ] + 1 ) + ( 1 - $refwt ) * ( $q_rank[ $i ] + 1 ) ) ** -1;
		$rank_score += ( $rank_diff ** 0.5 * $wt );
#		$rank_score += ( $rank_diff * $wt );
	}
	return $rank_score;
}

sub max{
	my $a = shift( @_ );
	my $b = shift( @_ );
	if( $a >= $b ){ return $a; }
	else{ return $b; }
}
