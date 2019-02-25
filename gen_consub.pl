#!/usr/bin/perl 

if( !$ARGV[ 0 ] ){ die "args:\tpdblist\targsfile\t<priority>\t<resfilelist>\t<ccp4list>\n"; }
$pdblist_name = shift( @ARGV ); #||
$argsfile = shift( @ARGV ); #||
$prio = shift( @ARGV ) || 0;
$resfilelist_name = shift( @ARGV ) || 0;
$ccp4list_name = shift( @ARGV ) || 0;
$pwd = `pwd`;

$runtag = ( split ' ', `grep \'tag \' $argsfile` )[ 1 ];
if( $runtag ){ $runtag = ".$runtag"; }
@argsnametags = split '\.', $argsfile;
pop( @argsnametags );
$nametag = join( '.', @argsnametags );
open OUT, ">$nametag.consub";

print OUT "
universe = vanilla
notification = Never
Executable = /work/chrisk/trunk/mini/bin/rotamer_repack.linuxgccrelease
Initialdir = $pwd
copy_to_spool = FALSE
";

@pdblist = `cat $pdblist_name`;
chomp( @pdblist );
if( $resfilelist_name ){
	@resfilelist = `cat $resfilelist_name`;
	chomp( @resfilelist );
}
if( $ccp4list_name ){
	@ccp4list = `cat $ccp4list_name`;
chomp( @ccp4list );
}
#@nat_pdblist = @pdblist;
#chomp( @nat_pdblist );
foreach ( 0..$#pdblist ){

	@pathparse = ( split '/', $pdblist[ $_ ]);
	$pdbname = $pathparse[ $#pathparse ];
	@parse = split '\.', $pdbname;
	pop( @parse );
	$pdb4 = $parse[ 0 ];
	$tag = join( '.', @parse );
	$outtag = "$tag$runtag";
	$mapfile = lc( $pdb4 ).'.ccp4';
#	print OUT "Arguments = \@$argsfile -s $pdblist[ $_ ] -resfile $resfilelist[ $_ ]\n";
	$args_condor = "Arguments = \@$argsfile -s $pdblist[ $_ ] ";
	if( $resfilelist_name ){ $args_condor = $args_condor . "-resfile $resfilelist[ $_ ] "; }
	if( $ccp4list_name ){ $args_condor = $args_condor . "-edensity:mapfile $ccp4list[ $_ ] "; } 
	print OUT "$args_condor\n";
	print OUT "Output = $outtag.out\n";
	print OUT "Log = $outtag.log\n";
	print OUT "Error = $outtag.err\n";
	print OUT "priority = $prio\n";
	print OUT "Queue\n";
}


