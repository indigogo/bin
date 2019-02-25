#!/usr/bin/perl 

if( !$ARGV[ 0 ] ){ die "args:\tanl_file\tdun_lib\t<n_sigmas(1)>\n"; }
if( $ARGV[ 0 ] eq '-' ){ @ARGV = <>; }
$anl_file = shift( @ARGV ); #||
$dunlib_file = shift( @ARGV ); #||
$nsig = shift( @ARGV ) || 1;
$d_pp = 10;

@anl = `cat $anl_file`;
@dun = `cat $dunlib_file`;

#rotparse anl
foreach $rotline( @anl ){
	%rotdata = {};
	@rotparse = split ' ', $rotline;
	shift( @rotparse );
	$pdb = shift( @rotparse );
	$resid = shift( @rotparse );
	$chain = shift( @rotparse );
	$resname = shift( @rotparse );

	#load anl rotline into hash
	while( $#rotparse >= 0 ){
		$tag = shift( @rotparse );
		if( $tag =~ /:$/ ){
			$tag =~ s/://;
			$val = shift( @rotparse );
			$rotdata{ $tag } = $val;
		}
	}
	print $rotline;
	#search dunlib w/ rotdata
	@nbr1 = ();
	@nbr2 = ();
	@nbr3 = ();
	@nbr4 = ();
#print "$nsig sigma:\n";
	foreach $dunline( @dun ){
		if( $dunline !~ /^$resname/ ){ next; }
		@dunparse = split ' ', $dunline;
		$phi = $dunparse[ 1 ];
#print "$rotdata{ 'phi' } $phi $phisig\n";
		if( &absdiff( $rotdata{ 'phi' } - $phi ) > ( $d_pp / 2 ) ){ next; }
#print "!!\n\n";
		$psi =$dunparse[ 2 ]; 
		if( &absdiff( $rotdata{ 'psi' } - $psi ) > ( $d_pp / 2 ) ){ next; }

		$count =$dunparse[ 3 ]; 
		$prob =$dunparse[ 8 ]; 
		$chi1 =$dunparse[ 9 ]; 
		$chi1sig =$dunparse[ 13 ]; 

		if( &absdiff( $rotdata{ 'chi1' } - $chi1 ) > $nsig * $chi1sig ){ next; }
		push( @nbr1, $dunline );
		$chi2 =$dunparse[ 10 ]; 
		$chi2sig =$dunparse[ 14 ]; 
		if( &absdiff( $rotdata{ 'chi2' } - $chi2 ) > $nsig * $chi2sig ){ next; }
		push( @nbr2, $dunline );
		$chi3 =$dunparse[ 11 ]; 
		$chi3sig =$dunparse[ 15 ]; 
		if( &absdiff( $rotdata{ 'chi3' } - $chi3 ) > $nsig * $chi3sig ){ next; }
		push( @nbr3, $dunline );
		$chi4 =$dunparse[ 12 ]; 
		$chi4sig =$dunparse[ 16 ]; 
		if( &absdiff( $rotdata{ 'chi4' } - $chi4 ) > $nsig * $chi4sig ){ next; }
		push( @nbr4, $dunline );
#			print "$dunline";
	}
	if( $#nbr4 >= 0 ){ print "chi4\n";foreach( @nbr4 ){ print $_; } }
	elsif( $#nbr3 >= 0 ){ print "chi3\n";foreach( @nbr3 ){ print $_; } }
	elsif( $#nbr2 >= 0 ){ print "chi2\n";foreach( @nbr2 ){ print $_; } }
	elsif( $#nbr1 >= 0 ){ print "chi1\n";foreach( @nbr1 ){ print $_; } }
	print "\n";
}

sub absdiff{

	my $a1 = shift( @_ );
	my $a2 = shift( @_ );

	$d = abs( $a1 - $a2 );
	if( $d > 180 ){ $d = 360 - $d; }
	return $d;
}


