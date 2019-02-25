#!/usr/bin/perl

if( !$ARGV[ 0 ] ){ die "args:\toutfile\n"; }
if( $ARGV[ 0 ] eq '-' ){ @ARGV = <>; }
$filename = shift( @ARGV ); #||
@fileparse = split( '\.', $filename );
pop( @fileparse );
$filetag = join( '\.', @fileparse );

`rot_anl_sort.pl $filename`;
print "low bfactor, no clash in native or min, min < 0.8 rmsd, rtmin > 1.0 rmsd\n";
`rot_anl_diff.pl $filetag.nat.out $filetag.min.out > $filetag.nat-min.out`;
`rot_anl_filter.pl $filetag.nat-min.out sc_bfactor lt 1.0 total_score lt 0.001 fa_rep gt -5.0 scauto_rmsd_nat lt 0.8 > $filetag.nat-min.fltr.out`;
`rot_anl_diff.pl $filetag.min.out $filetag.rtmin.out > $filetag.min-rtmin.out`;
`rot_anl_filter.pl $filetag.min-rtmin.out sc_bfactor lt 30.0 total_score lt 0.001 fa_rep gt -5.0 > $filetag.min-rtmin.fltr.out`;
`rot_anl_match.pl $filetag.nat-min.fltr.out and $filetag.min-rtmin.fltr.out > $filetag.nat-min.fltr_and_min-rtmin.fltr.out`;
`rot_anl_filter.pl $filetag.nat-min.fltr_and_min-rtmin.fltr.out scauto_rmsd_nat gt 1.0 > $filetag.min-rtmin.fail.out`;
`rot_anl_match.pl $filetag.min-rtmin.fail.out and $filetag.min.out > $filetag.min.fail.out`;
`nres_frac.pl $filetag.min-rtmin.fail.out $filetag.nat-min.fltr_and_min-rtmin.fltr.out > $filetag.fail.nres`;
