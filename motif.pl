#!/usr/bin/perl
if( $#ARGV < 1 ){ die "args:\tfilename\tlin_or_log\t<nrg_column>\t<kt>\t<freq_or_pssm>\n"; }
$filename = shift(@ARGV);
$type = shift( @ARGV );
$nrg = shift( @ARGV );
$kt = shift( @ARGV );
$dump_matrix = shift( @ARGV );

$nrg_sort = $nrg - 1;
@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');

if( $type eq 'log' ){
	@seqs = `grep '!!!' $filename | sort -n +$nrg_sort | awk '{print \$3}' `;
	@scores = `grep '!!!' $filename | sort -n +$nrg_sort | awk '{print \$$nrg}' `;
	#normalize scores to min,max
	$min_score = $scores[0];
	foreach $trial( 0..$#scores ){
		$scores[$trial] = ( $scores[$trial] - $min_score );
	}
}
else{
	@seqs = `grep '!!!' $filename | awk '{print \$3}' `;
}

foreach $seqpos(0..$#seq-1){
	foreach $resi(0..$#restypes){
		$scorematrix[$seqpos]{$restypes[$resi]} = 0;
	}
}


foreach $trial(0..$#seqs){
	@seq = split '', $seqs[$trial];
	foreach $seqpos(0..$#seq-1){
		if( $type eq 'log' ){ $scorematrix[$seqpos]{$seq[$seqpos]} += exp( -$scores[$trial] / $kt ); }
		elsif( $type eq 'lin' ){ $scorematrix[$seqpos]{$seq[$seqpos]} += 1; }
	}
}

if( $dump_matrix eq 'psfm' ){
	foreach $seqpos(0..$#seq-1){
		$norm_sum = 0;
		$info_sum = 0;
		# find sum of scores at seqpos
		foreach $resi(0..$#restypes){
			$norm_sum += $scorematrix[$seqpos]{$restypes[$resi]};
		}
		# normalize to frequency
		foreach $resi(0..$#restypes){
			if( $scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
				$scorematrix[$seqpos]{$restypes[$resi]} = $scorematrix[$seqpos]{$restypes[$resi]} / $norm_sum;
				print "$scorematrix[$seqpos]{$restypes[$resi]}\t";
			}
			else{ print "0\t"; }
		}
		print "\n";
	}
}

elsif( $dump_matrix eq 'pssm' ){
	$log_2 = log(2);
	$log_2_of20 = log(20) / $log_2;
	foreach $seqpos(0..$#seq-1){
		$norm_sum = 0;
		$info_sum = 0;
		# find sum of scores at seqpos
		foreach $resi(0..$#restypes){
			$norm_sum += $scorematrix[$seqpos]{$restypes[$resi]};
		}
		# normalize to frequency
		foreach $resi(0..$#restypes){
			if( $scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
				$scorematrix[$seqpos]{$restypes[$resi]} = $scorematrix[$seqpos]{$restypes[$resi]} / $norm_sum;
			}
		}
		$info_sum = $log_2_of20;
		$exp_info_sum = $log_2_of20;
		# calc info content at seqpos
		foreach $resi(0..$#restypes){
			if( $scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
				$info_sum += $scorematrix[$seqpos]{$restypes[$resi]} * log( $scorematrix[$seqpos]{$restypes[$resi]} ) / $log_2;
			}
		}
		# calc info weighted frequency at seqpos and rmsd b/t the two matrices
		foreach $resi(0..$#restypes){
			$scorematrix[$seqpos]{$restypes[$resi]} = $scorematrix[$seqpos]{$restypes[$resi]} * $info_sum;
			if( $scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
				print "$scorematrix[$seqpos]{$restypes[$resi]}\t";
			}
			else{ print "0\t"; }
		}
		print "\n";
	}
}

else{
	foreach $seqpos(0..$#seq-1){
		foreach $resi(0..$#restypes){
			$tmphash{$restypes[$resi]}=$scorematrix[$seqpos]{$restypes[$resi]};
		}

		@sorted = sort { $tmphash{$a} <=> $tmphash{$b} } keys %tmphash;

		foreach $resi(0..$#restypes){
			$seqmatrix[$seqpos][$resi] = $sorted[$resi];
		}
	}

	foreach $resi(0..$#restypes){
		foreach $seqpos(0..$#seq-1){
			print"$seqmatrix[$seqpos][$resi]\t";
		}
		print"\n";
	}
}
