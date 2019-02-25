#!/usr/bin/perl
if( !$ARGV[0] ){ die "args:\tpbase_path\n"; }
$db = shift( @ARGV );

@raw = `cat $db`;

foreach $entry( @raw ){
	$kin_col = ( split '\t', $entry )[ 5 ];
	@kins = split ';', $kin_col;
	foreach $kin( @kins ){
		$kin_hash{ $kin } += 1;
	}
}
foreach $key( keys %kin_hash ){
	print "$key\t$kin_hash{ $key }\n";
}
