#!/usr/bin/perl
if( $#ARGV < 1 ){ die "input:\tpath\tfilename\n"; }
$path = shift( @ARGV );
$name = shift( @ARGV );

$command = "find $path -name \'$name\' -type f | xargs rm";
print "$command\n";
`$command`;
