#!/usr/bin/perl
$path =  `pwd`;
chomp( $path );
$path =~ s/\/Users\/indigo//;
print $path." ".@ARGV."\n";
`rsync --copy-links -avrz -e "ssh -S /tmp/indigo-basil-socket" indigo\@10.1.64.64:/home/indigo/$path/@ARGV .`;
