#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tname\tdelim\tcolumn\toutname\n"; }
$name = shift( @ARGV );
$delim = shift( @ARGV );
$col = shift( @ARGV );
$out = shift( @ARGV );
`ls $name | sort -t '$delim' -nk $col | xargs cat > $out`;
