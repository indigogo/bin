#!/usr/bin/perl -w

if( !$ARGV[ 0 ] ){ die "args:file1\t<and||nand>\tfile2\n"; }
$f1name = shift( @ARGV ); #||
$nin = shift( @ARGV ); #||
$f2name = shift( @ARGV ); #||

@f1 = `cat $f1name`;
@f2 = `cat $f2name`;
chomp( @f1 );
chomp( @f2 );
foreach $line2( @f2 ){
	if( $nin eq 'and' ){ $fail = 1; }
	elsif( $nin eq 'nand' ){ $fail = 0; }
	foreach $line1( @f1 ){
		@checkparse = split ' ', $line1;
		@pdbparse = split /\//, shift( @checkparse );
		$pdbid = ( split /\./, pop( @pdbparse ) )[ 0 ];
		$resid = shift( @checkparse );
		$chain = shift( @checkparse );
		if( $line2 =~ /($pdbid)\S+\s+($resid)\s+($chain)\s+/ ){
			if( $nin eq 'and' ){ $fail = 0; }
			elsif( $nin eq 'nand' ){ $fail = 1; }
			last;
		}
	}
	if( $fail ){ next; }
	print "$line2\n";
}
