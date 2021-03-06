#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tfile.seq||file.psfm\tref_psfm\tnterm\t<bg_path>\t<dream>\t<exp>\n"; }

$filename = shift( @ARGV );
$ref_psfm = shift( @ARGV );
$nterm = shift( @ARGV );
$bg = shift( @ARGV ) || "/home/cking/work/bg/bg_std.psfm";
$dream = shift( @ARGV );
$exp = shift( @ARGV );

@parsed = split '\.', $filename;
$ext = pop( @parsed );
$runname = shift( @parsed );
foreach $field( @parsed ){ $runname = $runname.".".$field; }
if( $ext eq "spec" || $ext eq "seq" ){
	`gen_pssm.pl $filename psfm $nterm > $runname.psfm`;
	if( $diff ne '-' ){
		$diff = `diff_psfm.pl $ref_psfm $runname.psfm $dream`;
	}
	chomp( $diff );
	`weblogo.pl $filename $nterm \'$diff\'`;
}
else{
	`gen_seq.pl $runname.psfm 10000 > $runname.seq`;
	if( $diff ne '-' ){
		$diff = `diff_psfm.pl $ref_psfm $runname.psfm $dream`;
	}
	chomp( $diff );
	`weblogo.pl $runname.seq $nterm \'$diff\'`;
}
`divide_psfm.pl $bg $runname.psfm $exp > $runname.norm.psfm`;
`gen_seq.pl $runname.norm.psfm 10000 > $runname.norm.seq`;
if( $diff ne '-' ){
	$diff = `diff_psfm.pl $ref_psfm $runname.norm.psfm $dream`;
}
$nterm_norm = ( split ' ', `head -n 1 $runname.norm.psfm` )[ 0 ];
`weblogo.pl $runname.norm.seq $nterm_norm \'$diff\'`;
