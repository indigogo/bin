#!/usr/bin/perl

$pdbfile = shift( @ARGV );
$listname = shift( @ARGV );
@pdb = `cat $pdbfile`;
@list = `cat $listname`;

open PDB, ">$pdbfile.bfac";

for( $line = 0; $line <= $#pdb; $line++ ){
	if( !( substr( $pdb[ $line ], 0, 3 ) eq 'TER' ) ){
		$seqpos = substr( $pdb[ $line ], 22, 4 );
		$nrg = substr( $list[ $seqpos - 1 ], 0, 4 );
		substr( $pdb[ $line ], 62, 4 ) = substr( $list[ $seqpos - 1 ], 0, 4 );
	}
	print PDB $pdb[ $line ];
}
