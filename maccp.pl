#!/usr/bin/perl
$path =  `pwd`;
chomp( $path );
$path =~ s/\/gpfs\/DS3524-1\/WORK//;
$path = "ibin.baker:/Users".$path.'/';
`scp -r @ARGV $path\n`;
