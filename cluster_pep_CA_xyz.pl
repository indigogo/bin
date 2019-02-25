#!/usr/bin/perl

if( !$ARGV[0] ){ die "args:\t*.ca\tRMSD_cutoff\n"; }
$filename = shift( @ARGV );
$cutoff = shift( @ARGV );

@file = `cat $filename`;
#each peptide
foreach $line1( 0..( $#file - 1 ) ){
	@coords1 = split ' ', $file[ $line1 ];	
	$pdbname = shift( @coords1 );
	$has_twin = 0;
	#each other peptide
	foreach $line2( ( $line1 + 1 )..$#file ){
		@coords2 = split ' ', $file[ $line2 ];
		shift( @coords2 );
		$rmsd = 0;
		#CA coords
		for( $x = 0; $x <= $#coords1; $x += 1 ){	
			$rmsd += ( $coords2[ $x ] - $coords1[ $x ] )**2;
		}
		$n_atoms = ( $#coords1 + 1 ) / 3;
		$rmsd = sqrt( $rmsd / $n_atoms );
		if( $rmsd < $cutoff ){
			$has_twin = 1;
			last;
		}
	}
	if( $has_twin ){ next; }
	print "$pdbname\n";
}
