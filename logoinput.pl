#!/usr/bin/perl

$filename = shift(@ARGV);
$low = shift(@ARGV);

if($low){
        @seqs = `grep '!!!$low' $filename | awk '{print \$2}' `;
        @scores = `grep '!!!$low' -B 1 $filename | grep 'Total' | awk '{print \$5}' `;
}


else{
        @seqs = `grep '!!!\\B' $filename | awk '{print \$2}' `;
        @scores = `grep '!!!$low\\B' -B 1 $filename | grep 'Total' | awk '{print \$5}' `;
}



foreach $seq(0..$#seqs){
	foreach(0..-1*int($scores[$seq]-1)){
		print"$seqs[$seq]";
	}
}
