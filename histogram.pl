#!/usr/bin/perl  

sub usage {
die <<INTRO;
USAGE: histogram.pl   file_name [-m minimum_value_threshold -M Maximum_value_threshold -n column_offset -b bins -s bin_size  other_files_to_concatenate]
PURPOSE: extracts column of numbers from file and computes an histogram with specified ranges and bins.
OPTIONS: -n  first column n=0, second n=1 .... (negative numbers count back from last column!)
         -s bin_size.
         -b bins.  default is 10.  
         -m lower threshold value.  all values below this are lumped into first bin
         -M upper threshold value.  all values above this are lumped into last bin
         -h skip header value: ignores this many lines from head of file
TIP: to use as a pipe, use a dash (-) in place of filename.
charlie strauss 1999          
INTRO
}

warn "COMMAND: histogram.pl @ARGV\n";
# /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/
my ($opts,$args,$err) = opts::my_getopts('mMnbsh:');
@ARGV=@{$args}; my %FLAGS = %{$opts};

usage unless @ARGV==1  ; # file name remaining
 
shift if ($ARGV[0] eq '-') ;  # POSIX pipe detection, erase the dash
print (@ARGV ? "File: $ARGV[0] " : "STDIN pipe ");

use strict;  
my (@value_array, @histogram);
my ($i,$t);
my ($field1,$field2,$field3,$field4);
 
my $column = $FLAGS{opt_n};

if ($FLAGS{opt_h}) {
while ( int($FLAGS{opt_h}) ) {  # read header lines off of the file 
    die "short file " unless defined(<>);
    $FLAGS{opt_h}-= 1;
 
    }
}
print "column $column\n";
while (<>) { $t=  (split )[$column];  push @value_array, $t  if defined($t);   }
 
die 'empty file column ' unless @value_array; 
my ($begin_value,$end_value);

unless ( defined($FLAGS{opt_m}) && defined($FLAGS{opt_M})) { # unless both min and max are defined we have to sort data to find them
    @value_array = sort { $a <=> $b  } @value_array;
    $begin_value = $value_array[0];
    $end_value= $value_array[-1];
} 
 
$begin_value = defined($FLAGS{opt_m}) ? $FLAGS{opt_m} : $begin_value;  # use either user specified or minumum of data
$end_value = defined($FLAGS{opt_M}) ? $FLAGS{opt_M} : $end_value;      # use either user specified or maximum of data
if ($begin_value>$end_value) {  ($begin_value,$end_value) = ($end_value,$begin_value);}  # idiot proof

my $bins = $FLAGS{opt_b} || 10;
my $bin_size = $FLAGS{opt_s} || ($end_value-$begin_value)/$bins || 1;

if (($bin_size*($bins)+$begin_value)>$end_value) {$bins = ($end_value-$begin_value)/$bin_size; } # jjg 6/01: fixed this bug which occasionally produced output with the wrong number of bins
#if (($bin_size*($bins+1)+$begin_value)>$end_value) {$bins = ($end_value-$begin_value)/$bin_size; } # wrong!

my($lump_begin,$lump_end)=(0,0);
foreach $i (@value_array) {
   if ($i<$begin_value) {$lump_begin++;next}
   if ($i>$end_value) {$lump_end++;next}  
   $histogram[ int (   ($i-$begin_value)/$bin_size  ) ]++;
   }
 
( $field2,$field3)=($begin_value,$lump_begin);
  printf "<        %7.5g> %6u\n",(  $field2,$field3) if ($lump_begin);
print "____Interval______Counts_____%___\n";
for ($i=0;$i<$bins;$i++) {
   ( $field1,$field2,$field3,$field4) =  ($begin_value+$i*$bin_size , $begin_value+$i*$bin_size+$bin_size, $histogram[$i] || 0 , 100*($histogram[$i]  ||0)/$#value_array );
   printf "<%7.5g,%7.5g> %6u  %6.2f%%\n",( $field1,$field2,$field3,$field4);
   }
print "__________________________________\n";
( $field2,$field3)=($end_value,$lump_end);
 printf "<%7.5g        > %6u\n",(  $field2,$field3) if ($lump_end);
 


format =
<@####.### @####.###> @>>>>>
$field1,  $field2, $field3
.   
format BB =
@<<<<<<<< @####.###> @>>>>>
$field1,    $field2, $field3
.  

 
package opts;
   sub my_getopts {
  
# general purpose command line parser
# operates on global @ARGV
# call with string 'xyz:pdq' plus optional code to designate how to handle errors.
# where x y and z are command line switches that take arguments
# and p,d, &q are ones that do not take args.
# e.g. suppose contents of ARGV resulted from:
#  -x first_arg -pd -y second_arg not_an_arg also_not_arg -q -z third_arg  again_not_arg
# then return value is a hash containing:
# x => first_arg, y=>second_arg, z=>third_arg, p=>1,d=>1,q=>1
# plus an array containing (not_an_arg,also_not_arg,again_not_arg)
# $err flags if error occurs such as missing args
# 



     my($argumentative,$ignore_err) = @_;
    local( $_); my($first,$rest);
    my $err = 0;
    my ($with_args,$without_args) = split /:/ , $argumentative;
   
    my $wal = length $with_args;
    my $i=0;my $pos;
    my (%arg_hash,@not_args);
     while ( $i<=$#ARGV ) {
      
    #  print "$i $ARGV[$i] \n";
      if ( $ARGV[$i] =~ /^-(.)(.*)/ ) # does it start with a dash?
         {
 
	    ($first,$rest) = ($1,$2);
	     $pos = index($argumentative,$first);
        
 	    
	   if($pos < 0) 
             {  # did not match any arg ?
		if ($ignore_err<2) 
                 {  #
	        	print STDERR "Switch -$first  no such switch \n";
                	$err = -1;  # a soft error
			last unless ($ignore_err) ;
                 }
               
                $pos = $wal+1  #  pretend it is a non-argument type flag 
             }
	  
	   if($pos <= $wal ) 
	     {  # needs an argument 
	           
		if (!$rest) #if $rest blank then arg is the next ARGV element 
                  {   
			$i++; #will absorb this arg
                      
	                if ($i>$#ARGV) 
                           {  # got any more args?
			      print STDERR "Switch -$first requires an argument \n";
                             $err=1; 
                             last unless ($ignore_err >1) ;
                             $ARGV[$i] = 1;  # make up the arg for it}  
                              
                            
                           }
  			  $rest = $ARGV[$i];  
                         
 	               
                
                   }
              }
	        else # does not need an arg
              {  
                   if ($rest) # if more tags then recylce the argument remainder
                     {   
			$ARGV[$i--] = "-$rest";
                            
                     }
		       $rest = 1;
                     
              }
  		
	         
            

	      $arg_hash{"opt_$first"} = $rest;   # remember the arg

	 } # did not start with dash
           else # is not an arg, so save it
         {  
            
               push @not_args, $ARGV[$i];
            
         }
           $i++;  # next arg
       } #next while
          
     return (\%arg_hash, \@not_args,$err);
} #end sub

 
 
END
1             
