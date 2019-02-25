#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tfile\tcol(1)>\n"; }
$file = shift(@ARGV);
if( $file eq '-' ){
	@vals = <>;
}
else{
	$col = shift(@ARGV) || 1;
	@vals = `cat $file | awk \'{print \$$col}\' `;
}

$sum = 0;
foreach( 0..$#vals ){
	$sum = $sum + $vals[$_];
}
print"$sum\n";

