#!/usr/bin/perl
if( $#ARGV < 3 ){ die "args:\tfasta_sequence_filename\tpdb_template_filename\tpdb_template_chainID\t#_of_models\n"; }
$fasta_filename = shift( @ARGV );
$pdb_filename = shift( @ARGV );
$pdb_chain = shift( @ARGV );
$n_models = shift( @ARGV );

@fasta_file = `cat $fasta_filename`;
$got_fasta_name = 0;
$seq;
foreach $line( @fasta_file ){
	chomp( $line );
	if( $got_fasta_name == 1 ){
		$seq = $seq.$line;
	}
	if( index( $line, '>' ) == 0 ){
		$fasta_name = ( split '\|', ( split '>', $line )[ 1 ] )[ 0 ];
		$got_fasta_name = 1;
	}
}
open ALI, ">$fasta_name.ali";
print ALI ">P1;$fasta_name\nsequence\:$fasta_name\:\:\:\:\:\:\:0.00: 0.00\n$seq*\n";
close ALI;

$pdb_name = ( split '.pdb', $pdb_filename )[ 0 ];
open ALIGN, ">$fasta_name"."_$pdb_name.align1d.py";
print ALIGN "from modeller import *\n\n";
print ALIGN "env = environ()\n";
print ALIGN "aln = alignment(env)\n";
print ALIGN "mdl = model(env, file='$pdb_name', model_segment=('FIRST:$pdb_chain','LAST:$pdb_chain'))\n";
print ALIGN "aln.append_model(mdl, align_codes='$pdb_name', atom_files='$pdb_filename')\n";
print ALIGN "aln.append(file='$fasta_name.ali', align_codes='$fasta_name')\n";
print ALIGN "aln.align2d()\n";
print ALIGN "aln.write(file='$fasta_name"."_$pdb_name.ali', alignment_format='PIR')\n";
print ALIGN "aln.write(file='$fasta_name"."_$pdb_name.pap', alignment_format='PAP')\n";
close ALIGN;

open MODEL, ">$fasta_name"."_$pdb_name.model.py";
print MODEL "from modeller import *\n";
print MODEL "from modeller.automodel import *\n\n";
print MODEL "env = environ()\n";
print MODEL "a = automodel(env, alnfile='$fasta_name"."_$pdb_name.ali', knowns='$pdb_name', sequence='$fasta_name', assess_methods=(assess.DOPE))\n";
print MODEL "a.starting_model = 1\n";
print MODEL "a.ending_model = $n_models\n";
print MODEL "a.make()\n";
close MODEL;
