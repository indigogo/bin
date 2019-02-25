#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tsys_filename(w/ seqpos)\tmm-dd\t<nametag>\n"; };
$proteins_filename = shift( @ARGV );
$date = shift( @ARGV );
$tag = shift( @ARGV );
if( $tag ){ $tag = $tag."_"; }

#input like: superfamily/protein/pdbid.args
@proteins = `cat $proteins_filename`;
chomp( @proteins );
$n_proteins = $#proteins + 1;

print "Analyzing: spec res under 2A to ref\n";
@pics;
foreach $line( @proteins ){
#	$seqpos = ( split " ", $line )[ 1 ];
	$line = ( split " ", $line )[ 0 ];
	
	@protein_info = split '/', $line;
	$args = pop( @protein_info );
	$protein = ( split "$args", $line )[ 0 ];
	$pdb = ( split '.args', $args )[ 0 ];

	$dir = $tag.$pdb."_".$date;	
	$path = $protein.$dir.'/';

	print "$path\t";
	chdir "$path";
#	$seqpos = 'p'.$seqpos.'_rmsd:	[01]\.';
	$n_tot = ( split ' ',`cat data.*.spec | wc` )[ 0 ];
#	$n_under = ( split ' ',`grep \'$seqpos\' data.*.spec | wc` )[ 0 ];
	$n_under = ( split ' ',`grep \'total_rmsd:	[01]\\.\' data.*.spec | wc` )[ 0 ];
	$percent = 100 * $n_under / $n_tot;
	print "$percent%\n";

	chdir "/external2/home/cking/work/";
}

