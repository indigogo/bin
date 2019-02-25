#!/usr/bin/perl
if( $#ARGV < 0 ){ die "args:\tseq_file\t<nterm>\t<title>\t<prob||bits>\n"; }
$seqfile = shift( @ARGV );
@file = `cat $seqfile`;
@line = split ' ', $file[ 0 ];
#$col = 1;
if( $#line > 1 ){ $col = 2; }
$nterm = shift( @ARGV ) || -5;
$title = shift( @ARGV );
$type = shift( @ARGV ) || "prob";
@outparse = split '\.', $seqfile;
$outfile = $outparse[ 0 ];
foreach( 1..$#outparse - 1 ){
	$outfile = $outfile . "." . $outparse[ $_ ];
}
if( $type eq "bits" ){ $outfile = $outfile.".info"; }
#`cat $seqfile | awk \'{print \$$col}\' > $seqfile.seq`;
#`/work/chrisk/weblogo/seqlogo -f $seqfile.seq -s $nterm -h 8 -w 24 -F png -S -c -n -o $outfile -t "$title"`;
$cmd = "/work/chrisk/weblogo/seqlogo -f $seqfile -s $nterm -h 8 -w 24 -F png -c -n -o $outfile -t \"$title\"";
if( $type eq "prob" ){ $cmd = $cmd." -S "; }
`$cmd`;
