#!/usr/bin/perl

$infile = shift( @ARGV ) || 'data.spec';
# take lowest 1% sorted by score
$frac_cutoff = shift( @ARGV ) || 0.01;
$type = shift( @ARGV ) || "bind";

if( $type eq "total" ){ $string = "total_score:"; }
elsif( $type eq "bind" ){ $string = "binding_score:"; }

@line = split ' ', `grep -m 1 \'$string\' $infile`;
$scorecol = 0;
foreach( 0..$#line ){
	if( $line[ $_ ] eq $string ){
		$scorecol = $_ + 2;
	}
}

$n_samples = int( ( split ' ', `wc -l $infile` )[ 0 ] * $frac_cutoff );
@out = `awk \'{print \$1"\\t"\$2"\\t"\$$scorecol}\' $infile | sort -rn +2 | tail -n $n_samples`;
print @out;
