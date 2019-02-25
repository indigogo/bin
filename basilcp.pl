#!/usr/bin/perl
$path =  `pwd`;
chomp( $path );
$path =~ s/\/Users\/indigo\///;
`rsync --copy-links -avrz -e "ssh -S /tmp/indigo-basil-socket" @ARGV  indigo\@10.1.64.64:/home/indigo/$path`;
