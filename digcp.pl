#!/usr/bin/perl
$path =  `pwd`;
chomp( $path );
$path = "dig3:".$path.'/';
`scp -r @ARGV $path\n`;
