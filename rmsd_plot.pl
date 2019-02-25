#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tdata\ttag1\ttag2\t<regexp>\n"; }
$all = shift( @ARGV );
$rmsdtype = shift( @ARGV ) || "rms";
$type = shift( @ARGV ) || "score";
$grep = shift( @ARGV );

$rmsd = `ncol.pl $rmsdtype: $all`;
$score = `ncol.pl $type: $all`;
chomp( $rmsd ); chomp( $score );
$comm = "plot \"$all\" u $rmsd:$score";

if( $grep ){
	$regexp = $all.".regexp";
	`grep \'$grep\' $all > $regexp`;
	$comm = $comm.", \"$regexp\" u $rmsd:$score lt 3";
}

$comm = $comm."\npause -1\n";
`echo '$comm' > data.gplt`;
`gnuplot data.gplt`;
