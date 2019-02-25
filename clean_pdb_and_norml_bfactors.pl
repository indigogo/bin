#!/usr/bin/perl -w
#extracts all non-water atoms from pdb, print w/ normalized b-factors calc from David Smith et al., "Improved amino acid flexibility parameters", Protein Science (2003) 12:1060
if( $#ARGV < 0 ){ die "args:\tpdblist\n"; }

$pdblist_file = shift( @ARGV );
@pdblist = `cat $pdblist_file`;
chomp( @pdblist );
foreach $pdbfile( @pdblist ){
	@nameparse = split '\.', $pdbfile;
	$name = '';
	foreach $i( 0..$#nameparse-1 ){ $name = $name.$nameparse[ $i ]; }
	open PDB, ">$name.bnorm.pdb";
	#clean pdb, remove waters
	@pdb = `grep \'ATOM\\|HETATM\' $pdbfile | grep -v REMARK | grep -v HOH | grep -v REVDAT`;
	#get b-factors
	@b = ();
	foreach $atom( @pdb ){
		my $b = substr( $atom, 60, 6 );
		push( @b, $b );
	}
	#calc median absolute deviation (from median)
	@b_sort = sort( @b );
	$b_med = $b_sort[ int( $#b_sort / 2 + 1 ) ];
	@b_absdev = ();
	foreach $b( @b ){
		push( @b_absdev, abs( $b - $b_med ) );
	}	
	@b_absdev_sort = sort( @b_absdev );
	$b_absdev_medidx = int( $#b_absdev_sort / 2 + 1 );
	$b_absdev_med = $b_absdev_sort[ $b_absdev_medidx ];
	#remove outliers
	@is_outlier = ();
	$b_mean = 0;
	$n_count = 0;
	$outlier_thresh = 3.5;	#from Smith et al.
	if( $b_absdev_med == 0 ){ $b_absdev_med = 0.01; }
	foreach $b( @b ){
		$outlier_val = 0.6745 * ( ( $b - $b_med ) / $b_absdev_med ); #from Smith et al.
		if( $outlier_val < $outlier_thresh ){
			push( @is_outlier, 0 );
			$b_mean = $b_mean + $b;
			$n_count = $n_count + 1;
		}
		else{
			push( @is_outlier, 1 );
		}
	}
	$b_mean = $b_mean / ( $n_count );
	#calc sd
	$b_sd = 0;
	foreach $i( 0..$#b ){
		if( $is_outlier[ $i ] ){ next; }
		$b_sd = $b_sd + ( $b[ $i ] - $b_mean )**2;
	}
	$b_sd = sqrt( $b_sd / ( $n_count - 1 ) );
	#calc Z-scores	
	foreach $i( 0..$#b ){
		$z_score = ( $b[ $i ] - $b_mean ) / $b_sd;
		$z_score = sprintf( "%.2f" , $z_score );
		$z_score = sprintf( "% 6s" , $z_score );
		substr( $pdb[ $i ], 60, 6, $z_score );
#		print "$z_score\n";
		print PDB "$pdb[ $i ]";
	}
}
