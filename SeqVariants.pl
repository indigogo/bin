#!/usr/bin/perl -w
#=======

# lucasnivon@gmail.com 2009/12

use Cwd;

$cmdflag = shift( @ARGV );
@matches = @ARGV;

if ($cmdflag eq "-h") 
{
    print "\t Input list of designs. Output is sequence variation in form of a resfile. \n";
    print "\t First argument is flag: \n";
    print "\t -f full output =  shows all sequence variation \n"; 
    print "\t -r resfile output = shows each residue that appears only once for a resfile \n";
    print "\t -s short output = only outputs lines that vary\n";
    print "\t Example: SeqVariants.pl -f LIST\n"; 
 		die;   
} elsif( $#matches == 0 ){
    
    open (MATCHFILES, "< $matches[0]");
    chomp (@matchfiles = <MATCHFILES>);
} else{
		@matchfiles = @matches;
}

    
    for ($i=0; $i<@matchfiles; $i++)
    {
	open (MATCH,"<$matchfiles[$i]");
	# print "$matchfiles[$i]\n";
	foreach (<MATCH>)
	{
	    
	    #ATOM      1  N   PRO A   1      17.394  10.423  12.347  1.00  0.00
	    
	    # $1 is ATOM, $2 is residue name, $3 is sequence position
	    if ($_ =~ /(\w+)\s+\d+\s+\w+\s+(\w+)\s+\w+\s+(\d+)\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+/) {
		## only include ATOM lines
		$tag = substr($_,0,4);
		$resname = substr($_,17,3);
		$pos = substr($_,23,3);
		if (($tag =~ m/ATOM/) && ($pos != 900) ) { 
		    $matches_nD[$pos][$i]=$resname;
		    #print "found a match $tag $resname $pos $matches_nD[$pos][$i] \n";
		}
	    }
	}
    }

%map_to_one = (         'GLY' => 'G',
			'ALA' => 'A',
			'VAL' => 'V',
			'LEU' => 'L',
			'ILE' => 'I',
			'PRO' => 'P',
			'CYS' => 'C',
			'MET' => 'M',
			'HIS' => 'H',
			'PHE' => 'F',
			'TYR' => 'Y',
			'TRP' => 'W',
			'ASN' => 'N',
			'GLN' => 'Q',
			'SER' => 'S',
			'THR' => 'T',
			'LYS' => 'K',
			'ARG' => 'R',
			'ASP' => 'D',
			'GLU' => 'E',);

print "start\n";

$variation=0;  ## indicates that position had some variation found

for $i (1..$#matches_nD) {  ## cycle over positions
    $reslist = ""; #print "\n";
    for $j (0..$#{$matches_nD[$i]} ){   ## cycle over designs
        #print "$j $reslist $i Map to One: $map_to_one{$matches_nD[$i][$j]}\n";
       	$reslist = $reslist.$map_to_one{$matches_nD[$i][$j]};
    }
    $firstres = substr($reslist,0,1);
    
    for $j (0..$#{$matches_nD[$i]} ){   ## cycle over designs, find the variant positions
	if ($map_to_one{$matches_nD[$i][$j]} ne $firstres){
	    $variation=1;
	}
    }
    
    if ($cmdflag eq "-f"){
	$reslist = $reslist;
    }   elsif ($cmdflag eq "-r"){
	# get rid of repeat characters http://www.perlmonks.org/?node_id=353072
	my (%seen, $new_string);
	for my $char ( split // , $reslist ) {
	    next if $seen{$char} || $char !~ /^[A-Z]$/;
	    $seen{$char}++;
	    $new_string .= $char;
	    last if length $new_string == 26;
	}
	$reslist = $new_string;
    } 
    
# final output
    if ($variation){
	printf "%5d%2s%6s%1s\n",$i,"A"," PIKAA ",$reslist;
    } else {
	if ($cmdflag ne "-s"){
	    printf "%5d%2s%6s\n",$i,"A"," NATRO ";
	}
    }

    $variation=0;
    #print "\n";
}

