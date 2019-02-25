#!/usr/bin/perl

$file = shift( @ARGV );
$kt = shift( @ARGV );

@total_nrg_file = `grep \'!!!\' $file`;
@pep_nrg_file = `grep \'!!pep\' $file`;
$prot_nrg_file = `grep \'!!prot\' $file`;

foreach $i_line( 0.. $#total_nrg_file ){
	@scores = split ' ', $total_nrg_file[ $i_line ];
	foreach $i_score( 0..$#scores ){
		if( $scores[ $i_score ] eq "total_score:" ){ $total_nrgs[ $i_line ] = $scores[ $i_score+1 ];}
	}
}

foreach $i_line( 0.. $#pep_nrg_file ){
	@scores = split ' ', $pep_nrg_file[ $i_line ];
	foreach $i_score( 0..$#scores ){
		if( $scores[ $i_score ] eq "total_score:" ){ $pep_nrgs[ $i_line ] = $scores[ $i_score+1 ];}
	}
}

@scores = split ' ', $prot_nrg_file;
foreach $i_score( 0..$#scores ){
	if( $scores[ $i_score ] eq "total_score:" ){ $prot_nrg = $scores[ $i_score+1 ];}
}

$w = 0;
$z = 0;
foreach $nrg( @pep_nrgs ){
	$exp = exp( -$nrg / $kt );
	$w = $w + $nrg * $exp;
	$z = $z + $exp;
}
$pep_nrg_avg = $w / $z;

$w = 0;
$z = 0;
foreach $nrg( @total_nrgs ){
	$bind_nrg = $nrg - $pep_nrg_avg - $prot_nrg;
	$exp = exp( -$bind_nrg / $kt );
	$w = $w + $bind_nrg * $exp;
	$z = $z + $exp;
}
$bind_nrg_avg = $w / $z;

print "Boltz_avg_bind_nrg:\t$bind_nrg_avg\n";

