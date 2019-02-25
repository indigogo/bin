#!/usr/bin/perl

$filename = shift(@ARGV);
print"$filename\n\n";
$low = shift(@ARGV);

if($low){
        @seqs = `grep '!!!$low' $filename | awk '{print \$2}' `;
        @scores = `grep '!!!$low' -B 1 $filename | grep 'Total' | awk '{print \$5}' `;
}


else{
        @seqs = `grep '!!!\\B' $filename | awk '{print \$2}' `;
        @scores = `grep '!!!$low\\B' -B 1 $filename | grep 'Total' | awk '{print \$5}' `;
}


foreach $trial(0..$#seqs){
	@seq = split '', $seqs[$trial];
	foreach $res(0..$#seq-1){
		$scorematrix[$res]{$seq[$res]}+=$scores[$trial];
	}
}

@restypes = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y');



foreach $res(0..$#seq-1){
	foreach $resi(0..$#restypes){
		$tmphash{$restypes[$resi]}=$scorematrix[$res]{$restypes[$resi]};
	}
	@sorted = sort { $tmphash{$a} <=> $tmphash{$b} } keys %tmphash;
	foreach $resi(0..$#restypes){
		$seqmatrix[$res][$resi] = $sorted[$resi];
	}
}

foreach $resi(0..$#restypes){
	foreach $res(0..$#seq-1){
		print"$seqmatrix[$res][$resi]";
	}
	print"\n";
}
