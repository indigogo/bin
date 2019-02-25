#!/usr/bin/perl

if( !$ARGV[ 0 ] ){ die "args:\toutfile1\toutfile2\n"; }
if( $ARGV[ 0 ] eq '-' ){ @ARGV = <>; }
$filename1 = shift( @ARGV ); #||
$filename2 = shift( @ARGV ); #||

@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');

@nres_num = split ' ', `nres_vector.py $filename1`;
@nres_tot = split ' ', `nres_vector.py $filename2`;
foreach( 0..$#nres_tot ){
	$nres_frac[ $_ ] = $nres_num[ $_ ]  / $nres_tot[ $_ ];
	print "$restypes[ $_ ]\t$nres_frac[ $_ ]\n";
}
