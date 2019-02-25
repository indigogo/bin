#!/usr/bin/perl
if( $#ARGV < 0 ){ die "args:\tfilename\tpsfm||pssm||show||find_anchor\t<nterm>\t<exp>\n"; }
$filename = shift( @ARGV );
if( $filename eq '-' ){ @file = <>; }
else{ @file = `cat $filename`; }
$dump_matrix = shift( @ARGV );
$nterm = shift( @ARGV ) || 0;
$exp = shift( @ARGV );

@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');

# get seq data
@line = split ' ', $file[ 0 ];
if( $#line > 1 ){ $seqcol = 1; }
else{ $seqcol = 0; }
foreach $i( 0..$#file ){
	$seqs[ $i ] = ( split ' ', $file[ $i ] )[ $seqcol ];
}

# init matrix
@test_seq = split '', $seqs[0];
foreach $seqpos(0..$#test_seq){
	foreach $resi(0..$#restypes){
		$scorematrix[$seqpos]{$restypes[$resi]} = 0;
	}
}

# fill matrix
foreach $trial(0..$#seqs){
	@seq = split '', $seqs[$trial];
	foreach $seqpos(0..$#seq){
		$scorematrix[$seqpos]{$seq[$seqpos]} += 1;
	}
}

if( $exp ){
	foreach $seqpos(0..$#seq){
		$norm_sum = 0;
		# find sum of scores at seqpos
		foreach $resi(0..$#restypes){
			$norm_sum += $scorematrix[$seqpos]{$restypes[$resi]};
		}
		# normalize to frequency
		foreach $resi(0..$#restypes){
			$scorematrix[$seqpos]{$restypes[$resi]} = ( $scorematrix[$seqpos]{$restypes[$resi]} / $norm_sum ) ** $exp;
		}
	}
}

# calc frequency matrix
if( $dump_matrix eq 'psfm' ){
	foreach $seqpos(0..$#seq){
		$norm_sum = 0;
		# find sum of scores at seqpos
		foreach $resi(0..$#restypes){
			$norm_sum += $scorematrix[$seqpos]{$restypes[$resi]};
		}
		# normalize to frequency
		$pos = $seqpos + $nterm;
		print "$pos\t";
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

# calc info-weighted score matrix
elsif( $dump_matrix eq 'pssm' || $dump_matrix eq 'find_anchor' ){
	$log_2 = log(2);
	$log_2_of20 = log(20) / $log_2;
	$max_info_sum = 0;
	$anchor_pos = 0;
	foreach $seqpos(0..$#seq){
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
		# calc info content at seqpos
		foreach $resi(0..$#restypes){
			if( $scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
				$info_sum += $scorematrix[$seqpos]{$restypes[$resi]} * log( $scorematrix[$seqpos]{$restypes[$resi]} ) / $log_2;
			}
		}
		if( $dump_matrix eq 'find_anchor' ){
			if( $info_sum >= $max_info_sum ){
				$max_info_sum = $info_sum;
				$anchor_pos = $seqpos + $nterm;
			}
			next;
		}
		# calc info weighted frequency at seqpos
		$pos = $seqpos + $nterm;
		print "$pos\t";
		foreach $resi(0..$#restypes){
			$scorematrix[$seqpos]{$restypes[$resi]} = $scorematrix[$seqpos]{$restypes[$resi]} * $info_sum;
			if( $scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
				print "$scorematrix[$seqpos]{$restypes[$resi]}\t";
			}
			else{ print "0\t"; }
		}
		print "\n";
	}
	if( $dump_matrix eq 'find_anchor' ){ print "$anchor_pos\n"; }
}

# show amino acid matrix in std out
else{
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
