#!/usr/bin/perl
if( !$ARGV[ 0 ] ){
	print "args:\tsys_filename\tcutoff\tscoretype\tnametag||\"-\"\tmm-dd\t<show>\t<bg>\n";
	die "tag n_pep score cut prerelax cenwts censeq cenbb softwts finalwts exrot mcmin upwtinter farelax STKin SH2 SH3 PDZ YKin 1433 total\n";
}
$proteins_filename = shift( @ARGV );
$cutoff = shift( @ARGV );
$scoretype = shift( @ARGV );
if( $scoretype eq 'bind' ){ die "\"$scoretype\" is not a valid scoretype!\n" }
$tag = shift( @ARGV );
if( $tag eq '-' ){ $tag = ''; }
else{ $tag = $tag."_"; }
$date = shift( @ARGV );
$show = shift( @ARGV );
$bg = shift( @ARGV );

#input like: superfamily/protein/pdbid.args
@proteins = `cat $proteins_filename`;
chomp( @proteins );
$n_proteins = $#proteins + 1;

#gen bg norm data
if( $bg eq 'bg' ){
	if( `find bg/ -maxdepth 1 -type d -name $tag."bg_".$date` ){ $bg_path = "bg/".$tag."bg_".$date; }
	else{ $bg_path = "bg/bgclassic_bg_08-28"; }
	chdir "$bg_path";
	$bg_cutoff = $cutoff * 10;
#	$bg_cutoff = 0.01;
	if( !`find . -maxdepth 1 -type f -name \'data\\.spec\'` ){
		`cat data.*.spec > data.spec; rm data.*.spec`;
	}
	if( !`find . -maxdepth 1 -type f -name \'data\\.out\'` ){
		`cat data.*.out > data.out; rm data.*.out`;
	}
	if( !`find . -maxdepth 1 -type f -name \'data\\.err\'` ){
		`cat data.*.err > data.err; rm data.*.err`;
	}
	if( $scoretype ne 'byres' ){
		`pep_sort.pl data.spec $bg_cutoff $scoretype > cut.spec`;
	#	$nterm = `gen_pssm.pl cut.spec find_anchor`;
	#	chomp( $nterm );
	#	$nterm = -1 * $nterm;
		$nterm = -6;
		`gen_pssm.pl cut.spec psfm $nterm > cut.psfm`;
	}
	else{ `gen_byres_pssm.pl data.spec $nterm total $cutoff > cut.psfm`; }
	chdir "/home/cking/work/";
}

@pics;
@pics_norm;
$diff_total = 0;
$diff_norm_total = 0;
$nres_total = 0;
$maxbits_total = 0;
foreach $line( @proteins ){
	$nterm = 'find';
	@line = split ' ', $line;
	$args_path = $line[ 0 ];
	$ref_psfm = $line[ 1 ];
	$nterm = $line[ 2 ];

	@protein_info = split '/', $args_path;
	$args = pop( @protein_info );
	$protein = pop( @protein_info );
	if( $protein eq "bg" ){ next; }
	$system = ( split "$args", $args_path )[ 0 ];
	$pdb = ( split '.args', $args )[ 0 ];

	$dir = $tag.$pdb."_".$date;	
	$path = $system.$dir.'/';

	#check dir exists
	if( !`find $system  -maxdepth 1 -type d -name $dir` ){ die "Directory $path does not exists!\n"; }
	else{ chdir "$path"; }

	#first iter only! finish printing run info
	if( $line eq $proteins[ 0 ] ){
		#get n_peptides
		$n_peptides = ( split ' ', `grep 'n_peptides' $args` )[ 1 ];
		$n_specfiles = ( split ' ', `ls data.*.spec | wc` )[ 0 ];
		$n_peptides = $n_specfiles * $n_peptides;

		#parse args file data
		if( `grep 'fastrelax_input' $args` ){ $prerelax = "Y"; }
		else{ $prerelax = "N"; }
		$cen_wts = ( split ' ', `grep 'cen_wts' $args` )[ 1 ];
		if( `grep 'random_seq' $args` ){ $cen_seq = "rand"; }
		else{ $cen_seq = "ala"; }
		if( `grep 'gen_pep_bb_sequential' $args` ){ $cen_bb = "iter"; }
		else{ $cen_bb = "full"; }
		$soft_wts = ( split ' ', `grep 'soft_wts' $args` )[ 1 ];
		$final_wts = ( split ' ', `grep '\\:wts' $args` )[ 1 ];
		if( `grep '-ex2' $args` ){ $ex = "1,2"; }
		elsif( `grep '-ex1' $args` ){ $ex = "1"; }
		else{ $ex = "0"; }
		if( `grep 'mcmin_design' $args` ){ $mcmin_design = "Y"; }
		else{ $mcmin_design = "N"; }
		if( `grep 'upweight_interface' $args` ){ $upwt_packer = "Y"; }
		else{ $upwt_packer = "N"; }
		if( `grep 'test_no_farelax' $args` ){ $farelax = "N"; }
		else{ $farelax = "Y"; }

		#print rest of runtmie variables
		print "$tag\X_$date $n_peptides $scoretype $cutoff $prerelax $cen_wts $cen_seq $cen_bb $soft_wts $final_wts $ex $mcmin_design $upwt_packer $farelax ";
	}

	#sort peptides
	$runname = "$protein.$dir.$scoretype-$cutoff";
	if( !`find . -maxdepth 1 -type f -name \'data\\.spec\'` ){
		`cat data.*.spec > data.spec;`;
		`rm data.*.spec`; #what if not finished? will re-gen data.*.out then next analysis will overwrite w/ incomplete!
	}
	if( !`find . -maxdepth 1 -type f -name \'data\\.out\'` ){
		`cat data.*.out > data.out; rm data.*.out`;
	}
	if( !`find . -maxdepth 1 -type f -name \'data\\.err\'` ){
		`cat data.*.err > data.err; rm data.*.err`;
	}

	#find nterm
	if( $nterm eq 'find' ){
		$nterm = `gen_pssm.pl data.spec find_anchor`;
		chomp( $nterm );
		$nterm = -1 * $nterm;
	}

	# gen psfm
	if( $scoretype ne 'byres' ){
		`pep_sort.pl data.spec $cutoff $scoretype > $runname.spec`;
	#gen and score profile
		`gen_pssm.pl $runname.spec psfm $nterm > $runname.psfm`;
	}
	else{ `gen_byres_pssm.pl data.spec $nterm total $cutoff > $runname.psfm; gen_seq.pl $runname.psfm 10000 > $runname.seq`; }
	@diff_out = split ' ', `diff_psfm.pl $ref_psfm $runname.psfm`;
	$diff = $diff_out[ 0 ] / $diff_out[ 2 ];
	$diff_total += $diff_out[ 0 ];
	$maxbits_total += $diff_out[ 2 ];
	$nres_total += $diff_out[ 4 ];
	if( $scoretype ne 'byres' ){ `weblogo.pl $runname.spec 2 $nterm \'@diff_out\'`; }
	else{ `weblogo.pl $runname.seq 1 $nterm \'@diff_out\'`; } 
	push( @pics, "$path"."$runname.png" );

	#gen and score norm profile
	$runname_norm = $runname.".norm";
	if( $bg eq "self" ){
		`gen_pssm.pl data.spec psfm $nterm > data.psfm`;
		`divide_psfm.pl data.psfm $runname.psfm > $runname_norm.psfm`;
	}
	elsif( $bg eq "bg" ){
		`divide_psfm.pl /home/cking/work/$bg_path/cut.psfm $runname.psfm > $runname_norm.psfm`;
	}
	else{ `divide_psfm.pl /home/cking/work/bg/bg_std.psfm $runname.psfm > $runname_norm.psfm`; }
	`gen_seq.pl $runname_norm.psfm 10000 > $runname_norm.seq`;

	@diff_norm_out = split ' ', `diff_psfm.pl $ref_psfm $runname_norm.psfm`;
	$diff_norm = $diff_norm_out[ 0 ] / $diff_norm_out[ 2 ];
	$diff_norm_total += $diff_norm_out[ 0 ];
	`weblogo.pl $runname_norm.seq 1 $nterm \'@diff_norm_out\'`;
	push( @pics_norm, "$path"."$runname_norm.png" );
	if( !$bg ){ printf "%.3f ", $diff; }
	else{ printf "%.3f ", $diff_norm; }
#	`cp $runname.png ~/transfer`;
#	`cp $runname_norm.png ~/transfer`;

	chdir "/home/cking/work/";
}
$diff_total = $diff_total / $maxbits_total;
$diff_norm_total = $diff_norm_total / $maxbits_total;
if( !$bg ){ printf "%.3f\n", $diff_total; }
else{ printf "%.3f\n", $diff_norm_total; }
if( $show eq "show" ){
	`gimp @pics`;
	if( $bg ){ `gimp @pics_norm`; }
}

