#!/usr/bin/perl -w

if( !$ARGV[ 0 ] ){ die "args:\tanl_file\t< term >\t< lt||gt >\t< val >\n"; }
if( $ARGV[ 0 ] eq '-' ){ @ARGV = <>; }
$anl_file = shift( @ARGV ); #||
@filter_tags = ();
@filter_ineq= ();
@filter_vals = ();
while( $#ARGV > 0 ){
	push( @filter_tags, shift( @ARGV ) );
	push( @filter_ineq, shift( @ARGV ) );
	push( @filter_vals, shift( @ARGV ) );
}

@anl = `cat $anl_file`;
chomp( @anl );

#parse anl
foreach $line( @anl ){

	@parse = split ' ', $line;
	$fail = 0;
	while( $#parse >= 0 ){
		$tag = shift( @parse );
		if( $tag =~ s/:$// ){
			$val = shift( @parse );
			foreach $i( 0..$#filter_tags ){
				if( $tag eq $filter_tags[ $i ] ){
					if( $filter_ineq[ $i ] eq 'lt' && $val > $filter_vals[ $i ] ){ $fail = 1; }
					elsif( $filter_ineq[ $i ] eq 'gt' && $val <= $filter_vals[ $i ] ){ $fail = 1; }
					last;
					if( $i == $#filter_tags ){ die "$filter_tags[ $i ] not found at line:\n$line\n"; }
				}
			}
		}
		if( $fail == 1 ){ last; }
	}
	if( $fail == 1 ){ next; }
	print "$line\n";
}


