#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tblast_databse\tmodel_fasta\tPDBID\tchain\n"; }
$database = shift( @ARGV );
$fasta = shift( @ARGV );
$pdbid = shift( @ARGV );
$chain = shift( @ARGV ) || 'A';

@query = `/home/pbradley/bin/blast/blast-2.2.16/bin/blastpgp -d $database -i $fasta | grep '>gi.*$pdbid' -i -A 40 | grep 'Query'`;
$model_seq = ( split ' ', $query[ 0 ] )[ 2 ];
@sbjct = `/home/pbradley/bin/blast/blast-2.2.16/bin/blastpgp -d $database -i $fasta | grep '>gi.*$pdbid' -i -A 40 | grep 'Sbjct'`;
$templ_seq = ( split ' ', $sbjct[ 0 ] )[ 2 ];


$fasta_seq = `grep -v '>' $fasta`;
system( "/home/cking/pdbUtil/getPdb.pl -id $pdbid; gzip -d $pdbid.pdb.Z" );
$pdbfile = "$pdbid.$chain.pdb";
system( "grep 'ATOM................ $chain \\|TER................. $chain ' $pdbid.pdb | grep ' $chain ' > $pdbfile" );
$pdbfasta = "$pdbid.fasta";
system( "/home/cking/pdbUtil/getFastaFromCoords.pl -pdbfile $pdbfile -chain $chain > $pdbfasta" );
$pdb_seq = `grep -v '>' $pdbfasta`;
#find 1st pdb res, calc offset from 1st blast res, prepend <= aa's onto model and templ seqs
$model_r1 = int( ( split ' ', $query[ 0 ] )[ 1 ] );
$templ_r1 = int( ( split ' ', $sbjct[ 0 ] )[ 1 ] );
$pdb_r1 = ( split ' ', `grep 'ATOM' $pdbfile | head -n 1` )[ 5 ];

$templ_offset = $templ_r1 - $pdb_r1;
if( $templ_offset > 0 ){
	$templ_prepend = substr $pdb_seq, 0, $templ_offset;
}
$templ_seq = $templ_prepend.$templ_seq;

$model_offset = $model_r1 - 1;
#TODO add -'s if pdb nterm is longer
if( $model_offset >= $templ_offset ){
	$model_prepend = substr $fasta_seq, ( $model_offset - $templ_offset ), $templ_offset;
}
$model_seq = $model_prepend.$model_seq;

if( $templ_offset > $model_offset ){
	foreach( 0..( $templ_offset - $model_offset ) ){
		$model_seq = '-'.$model_seq;
	}
}
#TODO all above for cterm

print ">model\n$model_seq\n>template\n$templ_seq\n";
