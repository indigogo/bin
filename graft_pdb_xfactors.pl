#!/usr/bin/perl -w
#takes a file w/ int(resindex) vs. real(some value) and writes value[ i ] for residue[ i ] into bfactor field of pdb
if( $#ARGV < 0 ){ die "args:\tpdb\tdata_file\tresid_col(from 1)\tvalue_col(from 1)\n"; }

$pdbfile = shift( @ARGV );
$valfile = shift( @ARGV );
$idcol = shift( @ARGV );
$valcol = shift( @ARGV );
@nameparse = split '\.', $pdbfile;
$name = $nameparse[ 0 ];
foreach $i( 1..$#nameparse-1 ){ $name = $name.'.'.$nameparse[ $i ]; }
open PDB, ">$name.xfactor.pdb";
#load pdb, vals
@pdb = `grep \'ATOM\\|HETATM\' $pdbfile`;
@vals = `cat $valfile`;
#for each value
foreach $valpair( @vals ){
	$resid = ( split ' ', $valpair )[ $idcol - 1 ];
	$val = ( split ' ', $valpair )[ $valcol - 1 ];
	#write val into bfactor for residue
	foreach $i( 0..$#pdb ){
		$this_resid = substr( $pdb[ $i ], 22, 4 );
		if( abs( $resid - $this_resid ) < 0.0001 ){
			$val = sprintf( "%.2f" , $val );
			$val = sprintf( "% 6s" , $val );
			substr( $pdb[ $i ], 60, 6, $val );
		}
	}
}
foreach $i( 0..$#pdb ){
	print PDB "$pdb[ $i ]";
}

