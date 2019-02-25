#!/usr/bin/perl
$path =  `pwd`;
chomp( $path );
$path =~ s/\/Users\/indigo\///;
`rsync --copy-links -avrz -e "ssh -S /tmp/indigo-atlas-socket" @ARGV  indigo\@10.1.64.68:/mnt/tank/indigo/home/$path`;
