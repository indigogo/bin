#!/usr/bin/perl
#$path =  `pwd`;
#chomp( $path );
#$path =~ s/work/home/;
$path = "chrisk\@fw.bakerlab.org:/home/chrisk/";
`scp -r @ARGV $path\n`;
