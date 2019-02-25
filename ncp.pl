#!/usr/bin/perl

$path = "numbat:".( split 'external2', `pwd` )[1];
chomp( $path );
`scp -r @ARGV $path\n`;

