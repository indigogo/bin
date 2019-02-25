#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tpdb_filename\n"; }
$pdbname = shift( @ARGV );
@pdb = `cat $pdbname`;

`mv $pdbname $pdbname.dirty`;
open PDB, ">$pdbname";
for( $line = 0; $line <= $#pdb; $line++ ){
	if( substr( $pdb[ $line ], 13, 1 ) eq 'H' ){ next; }
	if( !( substr( $pdb[ $line ], 0, 4 ) eq 'ATOM' || substr( $pdb[ $line ], 0, 6 ) eq 'HETATM' || substr( $pdb[ $line ], 0, 3 ) eq 'TER' ) ){ next; }
	if( substr( $pdb[ $line ], 16, 1 ) eq 'B' ){ next; }
	if( substr( $pdb[ $line ], 16, 1 ) eq 'C' ){ next; }
	if( substr( $pdb[ $line ], 13, 3 ) eq 'OXT' ){ substr( $pdb[ $line ], 13, 3 ) = "OT "; }
	if( substr( $pdb[ $line ], 17, 3 ) eq 'HIS' ){ substr( $pdb[ $line ], 17, 3 ) = "HIE"; }
	if( substr( $pdb[ $line ], 21, 1 ) eq ' ' && !( substr( $pdb[ $line ], 0, 3 ) eq 'TER' ) ){ substr( $pdb[ $line ], 21, 1 ) = "A"; }
	if( substr( $pdb[ $line ], 16, 1 ) eq 'A' ){ substr( $pdb[ $line ], 16, 1 ) = " "; }
	print PDB $pdb[ $line ];
}
