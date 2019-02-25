#!/usr/bin/perl 

if( !$ARGV[ 0 ] ){ die "args:\tanl_file\tdun_rotlist\n"; }
if( $ARGV[ 0 ] eq '-' ){ @ARGV = <>; }
$anl_file = shift( @ARGV ); #||
$dunlib_file = shift( @ARGV ); #||
$within_rmsd = shift( @ARGV ) || 15;
$d_pp = 10;

@anl = `cat $anl_file`;
@dun = `cat $dunlib_file`;
chomp( @dun );

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
	#search dunlib w/ rotdata, bbindep thern bbdep
	foreach $i_bbdep( 0..1 ){
		%rmsdhash = ();
		$n_pp_bin = 0;
		foreach $i_dunline( 0..$#dun ){
			$rmsd = 0;
			$dunline = $dun[ $i_dunline ];
			@dunparse = split ' ', $dunline;
#if( $dunparse[ 2 ] !~ /^$resname/ ){ next; }
			$edens = $dunparse[ 5 ];
			if( $edens < 25.0 || $edens > 75.0 ){ next; }

			if( $i_bbdep ){
				$phi = $dunparse[ 9 ];
				if( $rotdata{ 'phi' } < $phi || $rotdata{ 'phi' } > $phi + $d_pp ){ next; }
				$psi =$dunparse[ 11 ]; 
				if( $rotdata{ 'psi' } < $psi || $rotdata{ 'psi' } > $psi + $d_pp ){ next; }
				$n_pp_bin += 1;
			}
			else{ $n_pp_bin += 1; }

			$chi1 =$dunparse[ 13 ];
			$rmsd += &absdiff( $rotdata{ 'chi1' } - $chi1 )**2; 
			$chi2 =$dunparse[ 15 ]; 
			$rmsd += &absdiff( $rotdata{ 'chi2' } - $chi2 )**2; 
			$chi3 =$dunparse[ 17 ]; 
			$rmsd += &absdiff( $rotdata{ 'chi3' } - $chi3 )**2; 
			$chi4 =$dunparse[ 19 ]; 
			$rmsd += &absdiff( $rotdata{ 'chi4' } - $chi4 )**2; 

#WARNING!: ARG only!!!
			$rmsd = sqrt( $rmsd / 4 );
			$rmsdhash{ $dunline } = $rmsd;
		}

		$n_within = 0;
		$i_sort = 0;
		foreach $this_dunline( sort { $rmsdhash{ $a } <=> $rmsdhash{ $b } } keys %rmsdhash ){
			if( $i_sort < 1 ){ print "$this_dunline\trmsd_tor:\t$rmsdhash{ $this_dunline }\t"; }
			$i_sort += 1;
			if( $rmsdhash{ $this_dunline } <= $within_rmsd ){ $n_within += 1; }
		}
		$n_within_ratio = $n_within/$n_pp_bin;
		print "n<$within_rmsd\_rmsd:\t$n_within/$n_pp_bin\tratio<$within_rmsd\_rmsd:\t$n_within_ratio\n";
	}
	print "\n";
}

sub absdiff{

	my $a1 = shift( @_ );
	my $a2 = shift( @_ );

	$d = abs( $a1 - $a2 );
	if( $d > 180 ){ $d = 360 - $d; }
	return $d;
}


