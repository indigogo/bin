#!/usr/bin/perl

if( !$ARGV[ 0 ] ){ die "args:\toutfile\n"; }
if( $ARGV[ 0 ] eq '-' ){ @ARGV = <>; }
$filename = shift( @ARGV ); #||
@fileparse = split( '\.', $filename );
pop( @fileparse );
$filetag = join( '\.', @fileparse );

@file = `cat $filename`;
#will assume nat, min, rtmin right now
@tags = ();
foreach $line( @file ){
	@parse = split( ' ', $line );
	$tag = ( split '\.', shift( @parse ) )[ 1 ];
	$tag =~ s/\://;
	$newtag = 1; foreach $this_tag( @tags ){ if( $this_tag eq $tag ){ $newtag = 0; } };
	if( $newtag ){ push( @tags, $tag ); }
	else{ last; };
}
foreach $this_tag( @tags ){ `rm $filetag.$this_tag.out` };
foreach $line( @file ){
	@parse = split( ' ', $line );
	$tag = ( split '\.', shift( @parse ) )[ 1 ];
	$tag =~ s/\://;
	$out = join( ' ', @parse );
	`echo $out >> $filetag.$tag.out`;
}
