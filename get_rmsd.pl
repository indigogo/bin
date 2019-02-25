#!/usr/bin/perl

if( !$ARGV[ 0 ] ){ die "args:\tpdb1\tchain1\tpdb2\tchain2\n"; }
$refname = shift( @ARGV );
$refchain = shift( @ARGV );
$predname = shift( @ARGV );
$predchain = shift( @ARGV );

@refca = `/work/chrisk/pdbUtil/getCAcoords.pl -pdbfile $refname -chain $refchain`;
@predca = `/work/chrisk/pdbUtil/getCAcoords.pl -pdbfile $predname -chain $predchain`;

if( $#refca != $#predca ){ die "nres mismatch!\n" }

$rmsd = 0;
foreach $ca( 0..$#refca ){
	@refcoords = split ' ', $refca[ $ca ];
	@predcoords = split ' ', $predca[ $ca ];
	$rmsd += ( $refcoords[ 0 ] - $predcoords[ 0 ] )**2;
	$rmsd += ( $refcoords[ 1 ] - $predcoords[ 1 ] )**2;
	$rmsd += ( $refcoords[ 2 ] - $predcoords[ 2 ] )**2;
}
$rmsd = sqrt( $rmsd / ( $#refca + 1 ) );
print "$rmsd\n";
