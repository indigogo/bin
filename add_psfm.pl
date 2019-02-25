#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tpsfm_list\t||\tpsfm1\tpsfm2\n"; }
@filenames;
#load mats from file list
if( $#ARGV == 0 ){
	$filename_list = shift( @ARGV );
	@filenames = `cat $filename_list`;
	chomp( @filenames );
}
#...or load from cmd line input
else{
	while( $#ARGV >= 0 ){
		push( @filenames, shift( @ARGV ) );
	}
}

$n_files = $#filenames + 1;
@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');

# init matrix
@test_psfm = `cat $filenames[ 0 ]`;
foreach $seqpos( 0..$#test_psfm ){
	$pos[ $seqpos ] = ( split ' ', $test_psfm[ $seqpos ] )[ 0 ];
	foreach $resi( 0..$#restypes ){
		$avg_psfm[ $seqpos ]{ $restypes[ $resi ] } = 0;
	}
}

foreach $filename( @filenames ){

	@psfm = `cat $filename`;
	chomp( @psfm );
	if( $#psfm != $#pos ){ die "$filename is different length!\n"; }

	foreach $seqpos( 0..$#psfm ){
		@freqs = split ' ', $psfm[ $seqpos ];
		shift( @freqs );
		if( $#freqs != $#restypes ){ die "$filename is not Nx20!\n"; }

		#normalize as you go
		foreach $resi( 0..$#freqs ){
			$avg_psfm[ $seqpos ]{ $restypes[ $resi ] } += ( $freqs[ $resi ] / $n_files );
		}
	}
}

#print
foreach $seqpos( 0..$#pos ){
	print "$pos[ $seqpos ]\t";
	foreach $resi( 0..$#restypes ){
		print "$avg_psfm[ $seqpos ]{ $restypes[ $resi ] }\t";
	}
	print "\n";
}

