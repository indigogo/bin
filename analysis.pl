#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tsys_filename\tmm-dd\tcutoff\tscoretype\t<nametag>\n"; };
$proteins_filename = shift( @ARGV );
$date = shift( @ARGV );
$cutoff = shift( @ARGV );
$scoretype = shift( @ARGV );
$tag = shift( @ARGV );
if( $tag ){ $tag = $tag."_"; }

#input like: superfamily/protein/pdbid.args
@proteins = `cat $proteins_filename`;
chomp( @proteins );
$n_proteins = $#proteins + 1;

print "$tag\X_$date $scoretype $cutoff * ";
@pics;
@pics_norm;
foreach $line( @proteins ){
	$nterm = 'find';
	@line = split ' ', $line;
	$args_path = $line[ 0 ];
	$ref_psfm = $line[ 1 ];
	$nterm = $line[ 2 ];

	@protein_info = split '/', $args_path;
	$args = pop( @protein_info );
	$protein = pop( @protein_info );
	$system = ( split "$args", $args_path )[ 0 ];
	$pdb = ( split '.args', $args )[ 0 ];

	$dir = $tag.$pdb."_".$date;	
	$path = $system.$dir.'/';

	#ask for overwrite directory
	if( !`find $system  -maxdepth 1 -type d -name $dir` ){
		print "Directory $path does not exists! Skip? (y/n):\t";
		$skip = <STDIN>;
		chomp( $skip );
		if( $skip eq 'y' ){ next; }
		else{ die; }
	}

	chdir "$path";
	`cat data.*.spec > data.spec; pep_sort.pl data.spec $cutoff $scoretype > cut.spec`;
	if( $line eq $proteins[ 0 ] ){
		$n_peptides = ( split ' ', `wc data.spec` )[ 0 ];
		print "$n_peptides\n";
	}
	if( $nterm eq 'find' ){
		$nterm = `gen_pssm.pl cut.spec find_anchor`;
		chomp( $nterm );
		$nterm = -1 * $nterm;
	}
	`gen_pssm.pl cut.spec psfm $nterm > cut.psfm`;
	`gen_pssm.pl data.spec psfm $nterm > data.psfm`;
	`divide_psfm.pl data.psfm cut.psfm > cut.norm.psfm`;
	`gen_seq.pl cut.norm.psfm 10000 > cut.norm.seq`;
	$cterm = $nterm - 1 + ( split ' ', `wc cut.psfm` )[ 0 ];
	print "$system$pdb ";
	print "$nterm/$cterm ";
	if( $ref_psfm ){
		$diff = `diff_psfm.pl $ref_psfm cut.psfm`; chomp( $diff );
		$diff_norm = `diff_psfm.pl $ref_psfm cut.norm.psfm`; chomp( $diff_norm );
		print "$diff "; print "Norm $diff_norm ";
	}
	`weblogo.pl cut.spec 2 $nterm \'$diff\' `;
	`mv cut.png $protein.$pdb.cut.png`;
	`weblogo.pl cut.norm.seq 1 $nterm \'$diff_norm\'`;
	`mv cut.norm.png $protein.$pdb.cut.norm.png`;
	push( @pics, "$path"."$protein.$pdb.cut.png" );
	push( @pics_norm, "$path"."$protein.$pdb.cut.norm.png" );
`cp $protein.$pdb.cut.png ~/transfer/`;
	chdir "/home/cking/work/";
	print "\n";
}

`gimp @pics`;
`gimp @pics_norm`;

