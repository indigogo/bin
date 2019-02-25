#!/usr/bin/perl

if( $#ARGV < 0 ){ die "args:\tspecfile\tfraction\tscoreterm\n"; }
$infile = shift( @ARGV ) || 'data.spec';
# take lowest 1% sorted by score
$frac_cutoff = shift( @ARGV ) || 0.01;
$type = shift( @ARGV ) || "total";

$string = $type."_score:";

@line = split ' ', `grep -m 1 \'$string\' $infile`;
$scorecol = 0;
foreach( 0..$#line ){
	if( $line[ $_ ] eq $string ){
		$scorecol = $_ + 2;
	}
}
if( $scorecol ==0 ){ die "$string not found!"; }

$n_samples = int( ( split ' ', `wc -l $infile` )[ 0 ] * $frac_cutoff );
@out = `sort -rnk $scorecol $infile | tail -n $n_samples`;
print @out;
