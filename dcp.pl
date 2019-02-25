#!/usr/bin/perl
$path = ( split 'cpb_', `pwd` )[ 1 ];
chomp( $path );
$path = "dormouse:/".$path.'/';
`scp -r @ARGV $path\n`;

