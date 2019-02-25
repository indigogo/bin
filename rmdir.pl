#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tsys_filename\tmm-dd\t<nametag>\n"; };
$proteins_filename = shift( @ARGV );
$date = shift( @ARGV );
$tag = shift( @ARGV );
if( $tag ){ $tag = $tag."_"; }

#input like: superfamily/protein/pdbid.args
@proteins = `cat $proteins_filename`;
chomp( @proteins );
$n_proteins = $#proteins + 1;

print "Deleting...\n";
foreach $line( @proteins ){
	@line = split ' ', $line;
	if( $line[ 1 ] ){ $ref_pssm = $line[ 1 ]; }
	if( $line[ 2 ] ){ $nterm = $line[ 2 ]; }
	$line = $line[ 0 ];

	@protein_info = split '/', $line;
	$args = pop( @protein_info );
	$protein = pop( @protein_info );
	$system = ( split "$args", $line )[ 0 ];
	$pdb = ( split '.args', $args )[ 0 ];

	$dir = $tag.$pdb."_".$date;	
	$path = $system.$dir.'/';

	`rm -rf $path`;
}


