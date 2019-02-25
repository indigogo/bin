#!/usr/bin/perl

if( $#ARGV < 0 ){ die "args:\tname\tbegin_time(ps)\tdelta_time(ps)\t<end_time(ps)>\n"; }
$name = shift( @ARGV );
$begin = shift( @ARGV );
$dt = shift( @ARGV );
if( $#ARGV >= 0 ){ $end = shift( @ARGV ); }

if( defined( $end ) ){
	`/work/bjelic/bin/GROMACS/software/bin/trjconv -s $name.md.tpr -f $name.md.xtc -o $name.md_.pdb -pbc mol -center -sep -b $begin -dt $dt -e $end < /work/chrisk/bin/trjconv.in `;
}
else{
	`/work/bjelic/bin/GROMACS/software/bin/trjconv -s $name.md.tpr -f $name.md.xtc -o $name.md_.pdb -pbc mol -center -sep -b $begin -dt $dt < /work/chrisk/bin/trjconv.in `;
}
