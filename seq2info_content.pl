#!/usr/bin/perl
if( $#ARGV < 0 ){ die "args:\tfilename\t<log_base(2)>\n"; }
$filename = shift( @ARGV );
if( $filename eq '-' ){ @file = <>; }
else{ @file = `cat $filename`; }
$base = shift( @ARGV ) | 2;

@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');

# get seq data
$seqcol = 1;
$seqcol = $seqcol - 1;
@line = split ' ', $file[ 0 ];
$seqcol = 0;
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

# calc info-weighted score matrix
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
	$info_sum = log( $#restypes + 1 ) / log( $base );
	# calc info content at seqpos
	foreach $resi(0..$#restypes){
		if( $scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
			$info_sum += $scorematrix[$seqpos]{$restypes[$resi]} * log( $scorematrix[$seqpos]{$restypes[$resi]} ) / log( $base );
		}
	}

	# calc info weighted frequency at seqpos
	$pos = $seqpos + 1;
	print "$pos\t";
	print "$info_sum\n";

#	foreach $resi(0..$#restypes){
#		$scorematrix[$seqpos]{$restypes[$resi]} = $scorematrix[$seqpos]{$restypes[$resi]} * $info_sum;
#		if( $scorematrix[$seqpos]{$restypes[$resi]} > 0 ){
#			print "$scorematrix[$seqpos]{$restypes[$resi]}\t";
#		}
#		else{ print "0\t"; }
#	}
#	print "\n";

}

