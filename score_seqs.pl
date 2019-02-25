#!/usr/bin/perl
if( $#ARGV < 1 ){ die "args:\tpssm_file\tseq_file\t<seq_col>\n"; }
$pssm_filename = shift(@ARGV);
$seq_filename = shift(@ARGV);
$seq_col = shift(@ARGV) || 1;
@pssm = `cat $pssm_filename`;
chomp( @pssm );


@seqs = `cat $seq_filename`;
chomp( @seqs );

@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');

# load the pssm
foreach $seqpos( 0..$#pssm ){
	@line = split ' ', $pssm[ $seqpos ];
	foreach $resi(0..$#restypes){
		$scorematrix[$seqpos]{$restypes[$resi]} = $line[ $resi + 1 ];
	}
}

# score each seq
foreach $trial(0..$#seqs){
	@seq = split '', ( split ' ', $seqs[ $trial ] )[ $seq_col ];
	$seq_score = 0;
	foreach $seqpos(0..$#seq){
		$seq_score += $scorematrix[$seqpos]{$seq[$seqpos]};
	}
	print "$seqs[$trial]";
	print "pssm_score:\t$seq_score\n";
}
