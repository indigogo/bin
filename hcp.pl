#!/usr/bin/perl
$path =  `pwd`;
chomp( $path );
$path = "hyrax1:/".$path.'/';
`scp -r @ARGV $path\n`;

