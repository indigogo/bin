#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tpdb_filename\n"; }
$pdbname = shift( @ARGV );
$pdbname =~ s/\.pdb$//;
@pdb = `cat $pdbname.pdb`;

open PDB, ">$pdbname.clean.pdb";
for( $line = 0; $line <= $#pdb; $line++ ){
	if( substr( $pdb[ $line ], 13, 1 ) eq 'H' ){ next; }
	if( !( substr( $pdb[ $line ], 0, 4 ) eq 'ATOM' || substr( $pdb[ $line ], 0, 6 ) eq 'HETATM' || substr( $pdb[ $line ], 0, 3 ) eq 'TER' ) ){ next; }
	if( substr( $pdb[ $line ], 16, 1 ) eq 'A' ){ substr( $pdb[ $line ], 16, 1 ) = " "; }
	if( substr( $pdb[ $line ], 16, 1 ) eq 'B' ){ next; }
	if( substr( $pdb[ $line ], 16, 1 ) eq 'C' ){ next; }
#	if( substr( $pdb[ $line ], 13, 3 ) eq 'OXT' ){ substr( $pdb[ $line ], 13, 3 ) = "OT "; }
#	if( substr( $pdb[ $line ], 21, 1 ) eq ' ' && !( substr( $pdb[ $line ], 0, 3 ) eq 'TER' ) ){ substr( $pdb[ $line ], 21, 1 ) = "A"; }
	print PDB $pdb[ $line ];
}
