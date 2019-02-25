#!/usr/bin/perl
if( $#ARGV < 3 ){ die "args:\tinfile\tfrac_cutoff\toutfile\tscp_path\n"; }
$infile = shift( @ARGV );
$frac_cutoff = shift( @ARGV );
$outfile = shift( @ARGV );
$path = shift( @ARGV );

$n_samples = int( ( split ' ', `grep \'!!!\' $infile | wc -l` )[ 0 ] * $frac_cutoff );
`grep \'!!!\' $infile | awk \'{print \$2"\\t"\$3"\\t"\$41}\' | sort -rn +2 | tail -n $n_samples > $outfile`;
