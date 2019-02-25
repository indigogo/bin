#!/usr/bin/perl
if( !$ARGV[0] ){ die "args:\tcommand\tn_procs\t||\tcommand\tproc1\tprocN\nwildcard is \'=\'\n"; }
$command = shift( @ARGV );
$n_procs = shift( @ARGV );
$first = 1;
if( $ARGV[0] ){
	$first = $n_procs;
	$n_procs = shift( @ARGV );
}

foreach $proc( $first..$n_procs ){
	my $command = $command;
	$index = index( $command, '=' );
	while( $index >= 0 ){
		substr( $command, $index, 1 ) = $proc;
		$index = index( $command, '=' );
	}
	`$command`;
#	print "$command\n";
}
