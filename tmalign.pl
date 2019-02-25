#!/usr/bin/perl
#Name of Chain_1: /work/krypton/DB/pdb/sl/3slpA.pdb                 
#Name of Chain_2: /work/krypton/DB/pdb/sl/3slpA.pdb                 
#Length of Chain_1:  226 residues
#Length of Chain_2:  226 residues
#
#Aligned length=  226, RMSD=   0.00, Seq_ID=n_identical/n_aligned= 1.000
#TM-score= 1.00000 (if normalized by length of Chain_1)
#TM-score= 1.00000 (if normalized by length of Chain_2)
#(You should use TM-score normalized by length of the reference protein)
my $native = $ARGV[0];
my $d = 1;
while(-e $ARGV[$d])
{
	my $print = $ARGV[0]."\t".$ARGV[$d];
	my @tm_lines = `/work/chrisk/bin/TMalign $native $ARGV[$d] -a`;
	my @len;
	my $aln_res;
	my $rmsd;
	for my $t (@tm_lines)
	{
		chomp($t);
		my @tm = split(/[\s\=\(\)\,\:]+/,$t);
		if($tm[0] eq "Length"){$print .= "\t".$tm[3]; push(@len,$tm[3]);}
		if($tm[0] eq "Aligned"){$print .= "\t".$tm[2]."\t".$tm[4]."\t".$tm[7]; $aln_res = $tm[2]; $rmsd = $tm[4];}
		if($tm[0] eq "TM-score"){$print .= "\t".$tm[1];}
		#if(index($t,"if normalized by length of Chain_") >= 0){print "\t".substr($t,10,7);}

		#obj03_trim_re.pdb	/lab/databases/ncbi/pdb/hu/3huqA.pdb	10	162	5	0.38	0.000	0.33566	0.03067
	}
	print $print."\n";
	#if($aln_res > 0)
	#{
	#	my $un_aln_res = $len[0] - $aln_res;
	#	my $rmsd_ = sprintf("%.3f",sqrt((($rmsd)**2 * $aln_res + (5**2) * $un_aln_res)/$len[0]));
	#	print $print."\t$rmsd_\n";
	#}
	$d++;
}
