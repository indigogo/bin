#!/usr/bin/perl

$filelist = shift( @ARGV );
$files = `cat $filelist | xargs`;

$out = shift( @ARGV );

`/home/pbradley/python/combine_png.py $out 1 3 $files`;
