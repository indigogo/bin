#!/usr/bin/perl
if( $#ARGV < 2 ){ die "args:\tref_seqs\tcomp_seqs\trmsd_or_list\n"; }
$ref_filename = shift(@ARGV);
$exp_filename = shift(@ARGV);
$type = shift(@ARGV);

$log_2 = log(2);
$log_2_of20 = log(20) / $log_2;


@seqs = `cat $ref_filename`;
@exp_seqs = `cat $exp_filename | awk \'{print \$1}\'`;
@exp_nrgs = `cat $exp_filename | awk \'{print \$2}\'`;

@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');

@seq = split '', $seqs[0];
foreach $seqpos(0..$#seq-1){
	foreach $resi(0..$#restypes){
		$scorematrix[$seqpos]{$restypes[$resi]} = 0;
		$exp_scorematrix[$seqpos]{$restypes[$resi]} = 0;
	}
}

# count n restypes at each seqpos for ref and exp
foreach $trial(0..$#seqs){
	@seq = split '', $seqs[$trial];
	foreach $seqpos(0..$#seq-1){
		$scorematrix[$seqpos]{$seq[$seqpos]} += 1;
	}
}
foreach $trial(0..$#exp_seqs){
	@exp_seq = split '', $exp_seqs[$trial];
	foreach $seqpos(0..$#exp_seq-1){
		$exp_scorematrix[$seqpos]{$exp_seq[$seqpos]} += 1;
	}
}

$rmsd = 0;
$n_elements = 0;
foreach $seqpos(0..$#seq-1){
	$norm_sum = 0;
	$info_sum = 0;
	$exp_norm_sum = 0;
	$exp_info_sum = 0;
	# find sum of scores at seqpos
	foreach $resi(0..$#restypes){
		$norm_sum += $scorematrix[$seqpos]{$restypes[$resi]};
		$exp_norm_sum += $exp_scorematrix[$seqpos]{$restypes[$resi]};
	}
	# normalize to frequency
	foreach $resi(0..$#restypes){
		if( $scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
			$scorematrix[$seqpos]{$restypes[$resi]} = $scorematrix[$seqpos]{$restypes[$resi]} / $norm_sum;
		}
		if( $exp_scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
			$exp_scorematrix[$seqpos]{$restypes[$resi]} = $exp_scorematrix[$seqpos]{$restypes[$resi]} / $exp_norm_sum;
		}
	}
	$info_sum = $log_2_of20;
	$exp_info_sum = $log_2_of20;
	# calc info content at seqpos
	foreach $resi(0..$#restypes){
		if( $scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
			$info_sum += $scorematrix[$seqpos]{$restypes[$resi]} * log( $scorematrix[$seqpos]{$restypes[$resi]} ) / $log_2;
		}
		if( $exp_scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
			$exp_info_sum += $exp_scorematrix[$seqpos]{$restypes[$resi]} * log( $exp_scorematrix[$seqpos]{$restypes[$resi]} ) / $log_2;
		}
	}
	# calc info weighted frequency at seqpos and rmsd b/t the two matrices
	foreach $resi(0..$#restypes){
		$scorematrix[$seqpos]{$restypes[$resi]} = $scorematrix[$seqpos]{$restypes[$resi]} * $info_sum;
		$exp_scorematrix[$seqpos]{$restypes[$resi]} = $exp_scorematrix[$seqpos]{$restypes[$resi]} * $exp_info_sum;
		if( $type eq "rmsd" ){
			$rmsd += ( $scorematrix[$seqpos]{$restypes[$resi]} - $exp_scorematrix[$seqpos]{$restypes[$resi]} )**2;
		}elsif( $type eq "informsd" ){
			$rmsd += $info_sum*( $scorematrix[$seqpos]{$restypes[$resi]} - $exp_scorematrix[$seqpos]{$restypes[$resi]} )**2;
		}
		$n_elements += 1;
#		$thisseqpos = $seqpos + 1;
#		$thisres = $restypes[$resi];
#		$thisscore = $scorematrix[$seqpos]{$restypes[$resi]};
#		print "$thisseqpos:$thisres:$thisscore\t";
#		print "\n";
	}
}
if( $type eq "rmsd" || $type eq "informsd" ){
	$rmsd = sqrt( $rmsd / $n_elements );
	print "$rmsd\n";
}
else{
# score each exp seq
	foreach $trial(0..$#exp_seqs){
		@exp_seq = split '', $exp_seqs[$trial];
		$seq_score = 0;
		foreach $seqpos(0..$#exp_seq-1){
			$seq_score += $scorematrix[$seqpos]{$exp_seq[$seqpos]};
		}
		$thisseq = $exp_seqs[$trial];
		$thisnrg = $exp_nrgs[$trial];
		chomp( $thisseq );
		print "$thisseq\t$seq_score\t$thisnrg\n";
	}
}


