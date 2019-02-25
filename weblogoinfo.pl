#!/usr/bin/perl
if( $#ARGV < 0 ){ die "args:\tseq_file\t<column>\t<nterm>\t<title>\n"; }
$seqfile = shift( @ARGV );
$col = shift( @ARGV ) || 1;
$nterm = shift( @ARGV ) || -5;
$title = shift( @ARGV );
@outparse = split '\.', $seqfile;
$outfile = $outparse[ 0 ];
foreach( 1..$#outparse - 1 ){
	$outfile = $outfile . "." . $outparse[ $_ ];
}
$outfile = $outfile . ".info";
`cat $seqfile | awk \'{print \$$col}\' > $seqfile.seq`;
`/home/cking/weblogo/seqlogo -f $seqfile.seq -s $nterm -h 8 -w 24 -F png -c -n -o $outfile -t "$title"`;
