#!/usr/bin/perl
if( $#ARGV < 3 ){ die "args:\tpbase_path\ttarget_name\tn_downstream\tn_upstream\n"; }
$db = shift( @ARGV );
$target_kin = shift( @ARGV );
$n_down = shift( @ARGV );
$n_up = shift( @ARGV );

@raw = `cat $db`;

foreach $entry( @raw ){
	$has_kin = 0;
	$kins = ( split '\t', $entry )[ 5 ];
	@kins = split ';', $kins;
	foreach $kin( @kins ){
		if( $kin eq $target_kin ){ $has_kin = 1; }
	}
	if( $has_kin == 1 ){
		$seq = ( split '\t', $entry )[ 1 ];
		@seq = split '', $seq;
		$pos = ( split '\t', $entry )[ 2 ];
		$start = $pos - $n_down;
		$end = $pos + $n_up;
		foreach $seqpos( $start-1..$end-1 ){
			if( $seqpos < 1 || $seqpos > $#seq ){
				print "X";
			}
			else{
				print "$seq[ $seqpos ]";
			}
		}
		print "\n";
	}
}
