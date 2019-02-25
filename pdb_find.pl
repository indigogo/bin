#!/usr/bin/perl
# searches through list of pdbs for structural homologs using TMalign
# only runs on DIG using sergey's scrt scripts!
# .tmalign output header
# pdb_1  pdb_2  len_1  len_2  align_len  aligned_rmsd  aligned_fraction_same_residue_type  tmscore_scaled_1  tmscore_scaled_2  tmscore_scaled_avg 
use File::Basename;
unless(exists $ARGV[1])
{
	print "pdb_find.pl <LIST> <PDB> <n_cores(20)>\n";
	die();
}
my $list = $ARGV[0];unless(-e $list){die("'$list' list does not exist");}
my $c = $ARGV[1];unless(-e $c){die("'$c' pdb does not exist");}
my $ncores = $ARGV[2] || 20;
my $C = basename( $c ).".".basename( $list );
open(PROCESS,">$C.run");
open(LIST,$list);
# need current working directory so parallel jobs know to come back to this dir 1st
use Cwd;
my $cwd = getcwd();
chomp( $cwd );
while($t = <LIST>)
{
	chomp($t);
	my $pdb = $t;
	# if filename does not begin with "/" and also file does not exist
	#  look for pdb file in hhsuite lab database
	if(substr($pdb,0,1) ne "/" and !-e $pdb)
	{
		my $d = substr($t,1,2);
		$pdb = "/lab/databases/hhsuite/pdb/$d/$t.pdb";
	}
	print PROCESS "cd $cwd; /work/chrisk/bin/tmalign.pl $c $pdb\n";
}
close(LIST);
close(PROCESS);
system( "/work/chrisk/bin/dighostfile.py $ncores 3 34" );
system("cat $C.run | /work/chrisk/bin/parallel --sshloginfile sshloginfile > $C.tmalign");
system("rm $C.run");
