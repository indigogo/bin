#!/usr/bin/perl

if( !$ARGV[ 0 ] ){ die "args:\tscorefile\tnterm\t<scoretype(binding)||total>\t<kT(1)>\t<outtype(psfm)>\n"; }
$filename = shift( @ARGV ); #||
$nterm = shift( @ARGV );
$scoretype_byres = shift( @ARGV );
$kt = shift( @ARGV ) || 1;
$outtype = shift( @ARGV );

#load file, init restypes
#if( $filename eq '-' ){ @file = <>; }
@file = `cat $filename`;
@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');

#get scoretype cols
$totalcol = `ncol.pl total_score: $filename`;
$pepcol = `ncol.pl binding_score: $filename`;
chomp( $totalcol ); chomp( $pepcol );

# line length, seq col, seq length
@test_parse = split ' ', $file[ 0 ];
$n_line = $#test_parse;
if( $n_line > 1 ){ $seqcol = 1; }
else{ $seqcol = 0; }
@test_seq = split '', $test_parse[ $seqcol ];
$n_seq = $#test_seq;

# init score matrix
foreach $seqpos( 0..$n_seq ){
	foreach $resi( 0..$#restypes ){
		$scorematrix[$seqpos]{$restypes[$resi]} = 0;
		$total[$seqpos]{$restypes[$resi]} = 0;
		$z_total[$seqpos]{$restypes[$resi]} = 0;
		$pep[$seqpos]{$restypes[$resi]} = 0;
		$z_pep[$seqpos]{$restypes[$resi]} = 0;
		$n_trial[$seqpos]{$restypes[$resi]} = 0;
	}
}

#get min score to avoid overflow
$min_total = ( split ' ', `sort -nk $totalcol $filename | head -n 1` )[ $totalcol - 1 ];

#iter over all seqs, subtr min_total from both scores
#fill up Nx20 matrices: total, pep, z_total, z_pep, n_trial 
foreach $lineno( 0..$#file ){
	@parse = split ' ', $file[ $lineno ];
	@seq = split '', $parse[ $seqcol ];
	foreach $seqpos( 0..$#seq ){
		#get scores, cols indexed from 1 in ncol.pl
		$restype = $seq[ $seqpos ];
		$total_this = $parse[ $totalcol - 1 ] - $min_total;
		$pep_this = $parse[ $pepcol - 1 ] - $min_total;
		#NOW AVG INSTEAD OF BOLTZ AVG BECAUSE NON-UNIFORM SEQ SAMPLING!
		#$z_total_this = ( exp( -1 * $total_this / $kt ) );
		$z_total_this = 1;
		#$z_pep_this = ( exp( -1 * $pep_this / $kt ) );
		$z_pep_this = 1;
		#add values to matrices
		$total[$seqpos]{$restype} += ( $total_this * $z_total_this );
		$z_total[$seqpos]{$restype} += $z_total_this;
		$pep[$seqpos]{$restype} += ( $pep_this * $z_pep_this );
		$z_pep[$seqpos]{$restype} += $z_pep_this;
		$n_trial[$seqpos]{$restype} += 1;
	}
}


#calc pssfm from other matrices
foreach $seqpos( 0..$n_seq ){
	$pos = $seqpos + $nterm;
	$z_prob = 0;

	#over all res
	foreach $resi( 0..$#restypes ){
		$prob_this = 0;
		if( $n_trial[$seqpos]{$restypes[$resi]} > 0 ){
			$total_this = $total[$seqpos]{$restypes[$resi]} / $z_total[$seqpos]{$restypes[$resi]};
			$pep_this = $pep[$seqpos]{$restypes[$resi]} / $z_pep[$seqpos]{$restypes[$resi]};
			$byres_this = $total_this - $pep_this;
			if( $scoretype_byres eq 'total' ){ $byres_this = $total_this; }
			#printf "$restypes[$resi]$seqpos\t%.3f\n", $byres_this;
			#ignore aa's that were never seen!
			if( $z_total[$seqpos]{$restypes[$resi]} > 0 ){ $prob_this = exp( -1 * $byres_this / $kt ); }
			else{ $prob_this = 0; }
		}
		$z_prob += $prob_this;
		$scorematrix[$seqpos]{$restypes[$resi]} = $prob_this;

	}#end resi

	#normalize probabilities
	foreach $resi( 0..$#restypes ){
		$scorematrix[$seqpos]{$restypes[$resi]} = $scorematrix[$seqpos]{$restypes[$resi]} / $z_prob;
	}

	#write psfm line
	if( $outtype ne 'show' ){
		print "$pos\t";
		foreach $resi( 0..$#restypes ){
			print "$scorematrix[$seqpos]{$restypes[$resi]}\t";
		}
		print "\n";
	}
	
}#end seqpos

#write alphabetical matrix to std out?
if( $outtype eq 'show' ){
	foreach $seqpos(0..$#seq){
		foreach $resi(0..$#restypes){
			$tmphash{$restypes[$resi]}=$scorematrix[$seqpos]{$restypes[$resi]};
		}

		@sorted = sort { $tmphash{$a} <=> $tmphash{$b} } keys %tmphash;

		foreach $resi(0..$#restypes){
			$seqmatrix[$seqpos][$resi] = $sorted[$resi];
		}
	}

	foreach $resi(0..$#restypes){
		foreach $seqpos(0..$#seq){
			print"$seqmatrix[$seqpos][$resi]\t";
		}
		print"\n";
	}
}


