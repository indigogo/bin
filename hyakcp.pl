#!/usr/bin/perl
$path =  `pwd`;
chomp( $path );
$path =~ s/\/gpfs\/DS3524-1\/[A-Z]+//;
`rsync --copy-links -avrz -e "ssh -S /tmp/chrisk1-hyak-socket" @ARGV  chrisk1\@hyak.washington.edu:/gscratch/baker/$path`;
