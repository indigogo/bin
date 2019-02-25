#!/usr/bin/perl
if( $#ARGV < 1 ){ die "args:\tcommand\targ1\t<arg2>\n"; }
$command = shift( @ARGV );
$arg1 = shift( @ARGV );
$arg2 = shift( @ARGV );

`find . -maxdepth 0 -name \'$arg1\' -print | xargs -l1 -i $command {} $arg2`;
