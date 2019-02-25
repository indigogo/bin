#!/usr/bin/perl
###CLIP THE TIP###
if( $#ARGV < 1 ){ die "args:\tpssm_file\tcomp_seqs\n"; }
$pssm_filename = shift(@ARGV);
$seq_filename = shift(@ARGV);
@pssm = `cat $pssm_filename`;
chomp( @pssm );


@seqs = `cat $seq_filename`;

@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');

# load the pssm
foreach $seqpos( 0..$#pssm ){
	foreach $resi(0..$#restypes){
		$scorematrix[$seqpos]{$restypes[$resi]} = ( split ' ', $pssm[ $seqpos ] )[ $resi ];
	}
}

# score each seq seq
@test_seq = split '', $seqs[0];
pop( @test_seq );
else{ $pep_begin = 0; $pep_end = $#test_seq - 1; }
foreach $trial(0..$#seqs){
	$thisseq = $seqs[$trial];
	chomp( $thisseq );
	@seq = split '', $thisseq;
	$seq_score = 0;
	foreach $seqpos($pep_begin..$pep_end){
		$this_res = $seq[$seqpos];
		$this_score = $scorematrix[$seqpos]{$this_res};
		$seq_score += $this_score;

#		print "$this_res:$this_score  ";
	}
	print "$thisseq\t";
	print "$seq_score\n";
}
