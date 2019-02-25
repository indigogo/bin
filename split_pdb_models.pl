#!/usr/bin/perl
if( $#ARGV < 0 ){ die "args:\tpdb_filename\n"; }

$pdb_filename = shift( @ARGV );
$pdb_name = ( split '\.', $pdb_filename )[ 0 ];
@pdb_file = `cat $pdb_filename`;
foreach $line( @pdb_file ){
	@parsed = split ' ', $line;
	if( $parsed[ 0 ] eq 'MODEL' ){
		open PDB, ">$pdb_name.$parsed[ 1 ].pdb";
	}
	print PDB "$line";
}
