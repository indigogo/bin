#!/usr/bin/perl
if( $#ARGV < 0 ){ die "args:\tpdb_model_filename\n"; }
$pdb_filename = shift( @ARGV );

$pdb_name = ( split '.pdb', $pdb_filename )[ 0 ];

open PROF, ">$pdb_name.profile.py";
print PROF "from modeller import *\n";
print PROF "from modeller.scripts import complete_pdb\n\n";
print PROF "env = environ()\n";
print PROF "env.libs.topology.read(file='\$(LIB)/top_heav.lib')\n";
print PROF "env.libs.parameters.read(file='\$(LIB)/par.lib')\n\n";
print PROF "mdl = complete_pdb(env, '$pdb_filename')\n\n";
print PROF "s = selection(mdl)\n";
print PROF "s.assess_dope(output='ENERGY_PROFILE NO_REPORT', file='$pdb_name.profile', normalize_profile=True, smoothing_window=15)\n";
close PROF;
