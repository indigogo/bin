#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\thmm\tfasta1\tfasta2\n"; }
$hmm = shift( @ARGV );
$seq1 = shift( @ARGV );
$seq2 = shift( @ARGV );
$name1 = substr `head -n 1 $seq1 | awk '{print \$1}'`, 1, 10;
$name2 = substr `head -n 1 $seq2 | awk '{print \$1}'`, 1, 10;
chomp( $name1 );
chomp( $name2 );

$aln1 = `~aticoll/hmmer-2.3.2.bin.amd-opteron-64-suse-linux/binaries/hmmpfam $hmm $seq1 | grep $name1 | grep -v Query | awk '{print \$3}' | xargs | sed 's/ //g' `;
$aln2 = `~aticoll/hmmer-2.3.2.bin.amd-opteron-64-suse-linux/binaries/hmmpfam $hmm $seq2 | grep $name2 | grep -v Query | awk '{print \$3}' | xargs | sed 's/ //g' `;
print ">$name1\n$aln1\n>$name2\n$aln2\n";
