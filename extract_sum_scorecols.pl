#!/usr/bin/perl 
#prints desired scorecols and their sum in last col
if( !$ARGV[ 0 ] ){ die "args:\t(foldx|SequenceDetail)*.fxout||*.byres.sc\t'tag'\n"; }
$filename = shift( @ARGV ); #||
@mytags = @ARGV;

if( $filename =~ /\.fxout/ ){
	if( $filename =~ /SequenceDetail/ ){
		$readingtag = 'amino acid';
		$headertag = 'amino acid';
	}
	else{
		$readingtag = '';
		$headertag = '';
	}
	$delim = '\t';
}
elsif( $filename =~ /\.(sc|out)/ ){
	$readingtag = 'SCORE:';
	$headertag = 'SCORE:';
	$delim = '\s+';
}
else{ die "extension must be fxout or sc/out!"; }

@file = `cat $filename`;
$reading = 0;
foreach $line( @file ){
	@parse = split /$delim/, $line;
	#find col idx for each tag
	if( !( $reading ) && $parse[ 0 ] eq $headertag ){
		$col = 0;
		foreach $tag( @parse ){
			foreach $mytag( @mytags ){
				if( $tag eq $mytag ){
					push( @cols, $col );
				}
			}
			$col++;
		}
		if( !$cols[ 0 ] ){ die "not tags found!\n"; }
	}
	#print lines
	if( $reading && $#parse > 0 && $line !~ /#END/ ){
		$colsum = 0;
		foreach $col( @cols ){
			print $parse[ $col ]."\t";
			$colsum += $parse[ $col ];
		}
		if( $#cols > 0 ){ print "$colsum"; }
		print "\n";
	}
	#start reading at first res
	if( $parse[ 0 ] eq $readingtag ){
		$reading = 1;
	}
}
