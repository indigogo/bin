#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tfile\tcol(1)\t<downsample\tboltzmann\tkt>\n"; }
$file = shift(@ARGV);
if( $file eq '-' ){
	@vals = <>;
}
else{
	$col = shift(@ARGV) || 1;
	$ds = shift(@ARGV) || 1;
	$boltz = shift(@ARGV);
	$kt = shift(@ARGV);
	if( $boltz eq "boltz" && $kt <= 0 ){ die "kt must be >= 0!\n"; }
	@vals = `cat $file | awk \'{print \$$col}\' `;

	if( $ds < 1 ){
		$i = 0;
		foreach( 0..$#vals ){
			if( rand() < $ds ){
				$dsvals[ $i ] = $vals[ $_ ];
				$i = $i + 1;
			}
		}
		@vals = @dsvals;
	}
}

$avg = 0;
$z = 0;
foreach( 0..$#vals ){
	if( $boltz eq "boltz" ){
		$w = exp( -$vals[$_] / $kt );
		$avg = $avg + $vals[$_] * $w;
	}
	else{
		$w = 1;
		$avg = $avg + $vals[$_];
	}
	$z = $z + $w;
}
$avg = $avg / $z;
print"$avg\n";

