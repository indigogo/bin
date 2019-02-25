#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tpsfm1\tpsfm2\nlower nterm first!"; }

$filename1 = shift( @ARGV );
$filename2 = shift( @ARGV );
$split = shift( @ARGV );

$n_files = 2;
@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');

@psfm1 = `cat $filename1`;
chomp( @psfm1 );
@psfm2 = `cat $filename2`;
chomp( @psfm2 );
$nterm = ( split ' ', $psfm1[ 0 ] )[ 0 ];
$cterm = ( split ' ', $psfm2[ $#psfm2 ] )[ 0 ];

$seqpos1 = 0;
$seqpos2 = 0;

foreach ( 0..( $cterm - $nterm ) ){
	@freqs1 = split ' ', $psfm1[ $seqpos1 ];
	@freqs2 = split ' ', $psfm2[ $seqpos2 ];
	$pos1 = shift( @freqs1 );
	$pos2 = shift( @freqs2 );
#	if( $#freqs1 != 19 ){ die "ref PSFM is not Nx20!\n"; }
	if( $seqpos1 > $#psfm1 ){
		print "$pos2\t@freqs2\n";
		++$seqpos2;
		next;
	}
	elsif( $pos1 < $pos2 ){
		print "$pos1\t@freqs1\n";
		++$seqpos1;
		next;
	}
	elsif( $pos1 == $pos2 ){
		if( $split ){
			if( $pos1 <= 0 ){ print "$pos1\t@freqs1\n"; }
			else{ print "$pos2\t@freqs2\n"; }
			
		}
		else{
			print "$pos1\t";
			foreach $f( 0..$#freqs1 ){
				$avg = ( $freqs1[ $f ] + $freqs2[ $f ] ) / 2;
				print "$avg ";
			}
			print "\n";
		}
		++$seqpos1;
		++$seqpos2;
		next;
	}
}

