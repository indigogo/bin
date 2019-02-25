#!/usr/bin/perl
$path =  `pwd`;
chomp( $path );
$path = "syd:".$path.'/';
`scp -r @ARGV $path\n`;
