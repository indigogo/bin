#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tpsfm_file\tn_seqs\t<label>\n"; }
$freq_filename = shift(@ARGV);
$n_seqs = shift(@ARGV);
$label = shift(@ARGV);

@freqs = `cat $freq_filename`;

chomp( @freqs );
if( $label eq "label" ){
	@restypes = split ' ', shift( @freqs );
}
else{
	@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');
}

# load the freq matrix, change to cumsum
@norms;
foreach $seqpos( 0..$#freqs ){
	$cumsum = 0;
	@line = split ' ', $freqs[ $seqpos ];
	#remove pos data
	shift( @line );
	foreach $resi(0..$#restypes){
		$cumsum += $line[ $resi ];
		$scorematrix[$seqpos]{$restypes[$resi]} = $cumsum;
	}
#	if( $cumsum ne 1 ){ print "cumsum == $cumsum @ line $seqpos\n"; }
	$norms[ $seqpos ] = $cumsum;
}

# generate random seqs from freq matrix
foreach( 0..$n_seqs-1 ){
	# gen random number, find where it is in freq matrix @ seqpos, assign that residue at seqpos
	foreach $seqpos( 0..$#freqs ){
		#random resi if all 0
		if( $norms[ $seqpos ] == 0 ){
			$random_resi = int( rand() * $#restypes );
			print "$restypes[$random_resi]";
		}
		#or find freq-weighted random resi
		else{
			$resindex = rand() * $norms[ $seqpos ];
			foreach $resi(0..$#restypes){
				if( $resindex <= $scorematrix[$seqpos]{$restypes[$resi]} ){
					print "$restypes[$resi]";
					last;
				}
			}
		}
	}
	print "\n";
}
