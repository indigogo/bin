#!/usr/bin/perl

use warnings;
use strict;

#
# Script to remove comments and protons from pdb files
# Skips atoms beginning H or number
#

unless ($ARGV[0])
    {
        die "Usage is pdbparse pdbname.ent > name.pdb";
    } 

my $filename = $ARGV[0];

open (PDBFILE, "$filename") || die "Cannot find file: $filename";

my $line;
my @temp;
while ( $line = <PDBFILE>)
    {
        #Skip all lines that are not atoms 
        unless ($line =~ m/^ATOM/) 
        {
             next;
        }
        @temp = split (/\s+/, $line);        
        #If the atom record starts with a digit or a H skip it
        if ( $temp[2] =~ m/^\d|^H/) 
        {
             next;
        }
	print $line;
    }
close (PDBFILE);
