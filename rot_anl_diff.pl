#!/usr/bin/perl

if( !$ARGV[ 0 ] ){ die "args:\tnatanl_file\tpertanl_file\t<score_filter>\t<rmsd_filter>\t<bfac_filter>\n"; }
if( $ARGV[ 0 ] eq '-' ){ @ARGV = <>; }
$natanl_file = shift( @ARGV ); #||
$pertanl_file = shift( @ARGV ); #||
$score_filter = shift( @ARGV ) || 999;
$rmsd_filter = shift( @ARGV ) || -1;
$bfac_filter = shift( @ARGV ) || 100;

$nodiff = 0;
if( $natanl_file eq $pertanl_file ){ $nodiff = 1; }

@natanl = `cat $natanl_file`;
@pertanl = `cat $pertanl_file`;
#TODO: assert same size

#parse anl
foreach $i( 0..$#natanl ){

	@natparse = split ' ', $natanl[ $i ];
	@pertparse = split ' ', $pertanl[ $i ];
	@out = ();

	shift( @natparse );
	push( @out,  shift( @pertparse ).' ' );

	#TODO: assert same resid, type
	shift( @natparse );
	push( @out,  shift( @pertparse ).' ' );
	shift( @natparse );
	push( @out,  shift( @pertparse ).' ' );
	shift( @natparse );
	push( @out,  shift( @pertparse ).' ' );
	shift( @natparse );
	push( @out,  shift( @pertparse ).' ' );

#	$fail = 1;
	$fail = 0;
	while( $#natparse >= 0 ){
		$nattag = shift( @natparse );
		$perttag = shift( @pertparse );
		if( $perttag =~ /:$/ ){
			if( $nattag ne $perttag ){ die "score tag mismatch at line $i! $nattag ne $perttag\n"; }
			push( @out,  "$perttag " );

		}
		else{
			#filters
			$lasttag = $out[ $#out ];
			$diff = $perttag - $nattag;
			if( $lasttag =~ /total_score/ && ( $diff > $score_filter ) ){ $fail = 1; }
			if( $lasttag =~ /sc3atom_rmsd/ && ( $perttag < $rmsd_filter ) ){ $fail = 1; }
			if( $lasttag =~ /sc_bfactor/ && ( $nattag > $bfac_filter ) ){ $fail = 1; }

			#print pert rmsd info, nat dun info
			if( $lasttag =~ /rmsd/ ){
				push( @out,  "$perttag " );
			}
			elsif( $lasttag =~ /(bfactor|phi|psi|chi)/ ){
				push( @out,  "$nattag " );
			}
			else{
				push( @out,  "$diff " );
			}
		}
	}
	push( @out,  "\n" );
	if( $fail ){ next; }
	$out = join( ' ', @out );
	print( "$out" );
}


