#!/usr/bin/perl

use Getopt::Long;
GetOptions("t=f"=>\$thinflag,"c=f"=>\$cflag,"r!"=>\$remove_dup,"f!"=>\$force_rename);

my $cutoff = 9999;
my $rand = 1.0;
if (defined $thinflag) { $rand = $thinflag; }
if (defined $cflag) { $cutoff = $cflag; }
if ($rand > 1.0) { $rand /= 100; } # take as percent

print STDERR "scorecut = $cutoff\n";
print STDERR "thinning = $rand\n";
print STDERR "removing duplicate tags\n" if $remove_dup;
print STDERR "renaming\n" if $force_rename;

my $filenum = 0;
my $doneheader = 0;
my $struct_count = 0;

my @silentfiles = ();

foreach my $arg (@ARGV) {
	if (substr($arg,0,1) eq '@') {
		my $listfile = substr($arg,1);
		open( INLIST , $listfile ) || die "Cannot open $listfile\n";
		while (my $line = <INLIST>) {
			chomp $line;
			push @silentfiles, $line;
		}
	} else {
		push @silentfiles, $arg;
	}		
}


foreach my $filename (@silentfiles) {

	print STDERR $filename."\n";
	open( INSILENT , $filename ) || die "Cannot open $filename\n";

	my $tag="XXXX  XXXX";
	my %processed_tags = ();

	while (my $line = <INSILENT>) {
		chomp $line;
		if ($line =~ /^SEQUENCE/ && $doneheader == 0) {
			print $line."\n";
		} elsif ($line =~ /^SCORE:\s+(\S+)\s+.*\s(\S+)\s*$/) {
			if ($line !~ /description/) {
				#print STDERR "$1 =?= $cutoff \n";

				#check cutoff
				if ($1 < $cutoff && (!defined $processed_tags{$2} || !$remove_dup) && rand()<$rand ) {
					$tag = $2;
					#print STDERR $tag."\n";
					$filenum++;
					$processed_tags{$2} = 1;
					$struct_count++;
					if ($force_rename) {
						$line =~ s/ $tag/ S_$filenum/;
					} else {
						$line = $line."_$filenum";
					}
					print $line."\n";
				} else {
					
					#if ($1 <  $cutoff) { print STDERR "Skipping $2 ... duplicate tag.\n"; }
					#else { print STDERR "Skipping $2 ... score above threshold.\n"; }
					$tag = "XXXX  XXXX";
				}
			} elsif ($doneheader == 0)  {
				$doneheader = 1;
				print $line."\n";
			}
		} elsif ($line =~ /$tag/) {
			if ($force_rename) {
				$line =~ s/ $tag/ S_$filenum/;
			} else {
				$line = $line."_$filenum";
			}
			print $line."\n";
		}
		#else {
		 #print $tag."***".$line."\n";
		#	if ($line =~ /^FOLD_TREE/ || $line =~ /^RT/ ) {
		#		print $line."\n";
		#	}
		#}
	}
}

print STDERR "Processed $struct_count structures in ".($#silentfiles+1)." files.\n";
