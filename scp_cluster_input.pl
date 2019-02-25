#!/usr/bin/perl
if( $#ARGV < 3 ){ die "args:\tinfile\tfrac_cutoff\toutfile\tscp_path\n"; }
$infile = shift( @ARGV );
$frac_cutoff = shift( @ARGV );
$outfile = shift( @ARGV );
$path = shift( @ARGV );

`( echo \'$outfile\'; cat $outfile | awk \'{print \$1}\'; echo \'$path\' ) | xargs scp`;
