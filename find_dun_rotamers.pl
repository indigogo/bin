#!/usr/bin/perl 

if( !$ARGV[ 0 ] ){ die "args:\tanl_file\tdun_rotlist\t<n_sigmas(1)>\n"; }
if( $ARGV[ 0 ] eq '-' ){ @ARGV = <>; }
$anl_file = shift( @ARGV ); #||
$dunlib_file = shift( @ARGV ); #||
$nsig_tot = shift( @ARGV ) || 1;
$d_pp = 10;
$chisig = 5;

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
	foreach $nsig( 1..$nsig_tot ){
		print "$nsig sigma:\n";
		foreach $dunline( @dun ){
			@dunparse = split ' ', $dunline;
#if( $dunparse[ 2 ] !~ /^$resname/ ){ next; }
			$edens = $dunparse[ 5 ];
			if( $edens < 25.0 || $edens > 75.0 ){ next; }
			$phi = $dunparse[ 9 ];
			if( &absdiff( $rotdata{ 'phi' } - $phi ) > ( $d_pp / 2 ) ){ next; }
			$psi =$dunparse[ 11 ]; 
			if( &absdiff( $rotdata{ 'psi' } - $psi ) > ( $d_pp / 2 ) ){ next; }

			$chi1 =$dunparse[ 13 ]; 
			if( &absdiff( $rotdata{ 'chi1' } - $chi1 ) > $nsig * $chisig ){ next; }
			push( @nbr1, $dunline );
			$chi2 =$dunparse[ 15 ]; 
			if( &absdiff( $rotdata{ 'chi2' } - $chi2 ) > $nsig * $chisig ){ next; }
			push( @nbr2, $dunline );
			$chi3 =$dunparse[ 17 ]; 
			if( &absdiff( $rotdata{ 'chi3' } - $chi3 ) > $nsig * $chisig ){ next; }
			push( @nbr3, $dunline );
			$chi4 =$dunparse[ 19 ]; 
			if( &absdiff( $rotdata{ 'chi4' } - $chi4 ) > $nsig * $chisig ){ next; }
			push( @nbr4, $dunline );
		}
		if( $#nbr4 >= 0 ){ print "chi4\n";foreach( @nbr4 ){ print $_; } }
		elsif( $#nbr3 >= 0 ){ print "chi3\n";foreach( @nbr3 ){ print $_; } }
		elsif( $#nbr2 >= 0 ){ print "chi2\n";foreach( @nbr2 ){ print $_; } }
		elsif( $#nbr1 >= 0 ){ print "chi1\n";foreach( @nbr1 ){ print $_; } }

		print "\n";
	}
}

sub absdiff{

	my $a1 = shift( @_ );
	my $a2 = shift( @_ );

	$d = abs( $a1 - $a2 );
	if( $d > 180 ){ $d = 360 - $d; }
	return $d;
}


