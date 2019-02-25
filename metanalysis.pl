#!/usr/bin/perl
if( !$ARGV[ 0 ] ){
	print "args:\tsys_filename\tcutoff||kt\tscoretype\tnametag||\"-\"\tmm-dd\t<show>\t<bg>\t<dream>\t<n_ensemble>\t<log_norm>\n";
	die "tag n_pep score cut prerelax cenwts censeq cenbb softwts finalwts exrot mcmin upwtinter farelax \n";
}
$proteins_filename = shift( @ARGV );
$cutoff = shift( @ARGV );
$scoretype = shift( @ARGV );
if( $scoretype eq 'bind' ){ die "\"$scoretype\" is not a valid scoretype!\n" }
$tag = shift( @ARGV );
if( $tag eq '-' ){ $tag = ''; }
else{ $tag = $tag."."; }
$date = shift( @ARGV );
$show = shift( @ARGV );
$bg = shift( @ARGV );
$dream = shift( @ARGV );
$n_seq_args = shift( @ARGV ) || 1;
$log_norm = shift( @ARGV );
$norm_script = "divide_psfm.pl";
$data2logo_script = "data2logo.pl";
if( $log_norm eq 'log' ){
	$norm_script = "divide_psfm.log.pl";
	$data2logo_script = "data2logo.log.pl";
}
#$ensemble = shift( @ARGV );
$all_dir;
$all_path;

#input like: superfamily/protein/pdbid.args
@proteins = `cat $proteins_filename`;
chomp( @proteins );
$n_proteins = $#proteins + 1;

$home = `pwd`;
chomp( $home );

#gen bg norm data
if( $bg && $bg ne '-' && $bg ne 'self' ){
	$bg_path = $bg;
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

	if( $n_seq_args > 1 ){
		@ensemble_psfms = ();
		@ensemble_specs = ();
	}

	foreach $n_arg( 1..$n_seq_args ){

		$dir = $tag.$pdb.".".$date;
		if( $n_seq_args > 1 ){ $dir = $tag.$pdb.".".$n_arg.".".$date; }
		$path = $system.$dir.'/';
		$all_path = $path;

#check dir exists
		if( $n_seq_args > 1 ){
			$all_dir = $tag.$pdb."."."all".".".$date;
			$all_path = $system.$all_dir.'/';
			if( !`find $system  -maxdepth 1 -type d -name $all_dir` ){ `mkdir $all_path`; }
		}
		if( !`find $system  -maxdepth 1 -type d -name $dir` ){ die "Directory $path does not exists!\n"; }
		else{ chdir "$path"; }

#sort peptides
		$runname = "$protein.$dir.$scoretype-$cutoff";
		if( !`find . -maxdepth 1 -type f -name \'data\\.spec\'` ){
			`cat data.*.spec >> data.spec;`;
			`rm data.*.spec`; 
		}
		if( !`find . -maxdepth 1 -type f -name \'data\\.out\'` ){
			`cat data.*.out >> data.out;`;
			`rm data.*.out`;
		}
		if( !`find . -maxdepth 1 -type f -name \'data\\.err\'` ){
			`cat data.*.err >> data.err`;
			`rm data.*.err`;
		}

#first iter only! finish printing run info
		if( ( $line eq $proteins[ 0 ] && $n_seq_args == 1 )  || ( $n_seq_args > 1 && $n_arg == 1 ) ){
#get n_peptides
			#$n_peptides = ( split ' ', `wc data.spec` )[ 0 ];

#parse args file data
			
#			if( `grep 'fastrelax_input' $args` ){ $prerelax = "Y"; }
#			else{ $prerelax = "N"; }
#			$cen_wts = ( split ' ', `grep 'cen_wts' $args` )[ 1 ];
#			if( `grep 'random_seq' $args` ){ $cen_seq = "rand"; }
#			else{ $cen_seq = "ala"; }
#			if( `grep 'gen_pep_bb_sequential' $args` ){ $cen_bb = "iter"; }
#			else{ $cen_bb = "full"; }
#			$soft_wts = ( split ' ', `grep 'soft_wts' $args` )[ 1 ];
#			$final_wts = ( split ' ', `grep '\\:wts' $args` )[ 1 ];
#			if( `grep '-ex2' $args` ){ $ex = "1,2"; }
#			elsif( `grep '-ex1' $args` ){ $ex = "1"; }
#			else{ $ex = "0"; }
#			if( `grep 'mcmin_design' $args` ){ $mcmin_design = "Y"; }
#			else{ $mcmin_design = "N"; }
#			if( `grep 'upweight_interface' $args` ){ $upwt_packer = "Y"; }
#			else{ $upwt_packer = "N"; }
#			if( `grep 'test_no_farelax' $args` ){ $farelax = "N"; }
#			else{ $farelax = "Y"; }
#			print "$all_dir $n_peptides $scoretype $cutoff $prerelax $cen_wts $cen_seq $cen_bb $soft_wts $final_wts $ex $mcmin_design $upwt_packer $farelax ";
			print "$tag.$date/$scoretype-$cutoff $bg $log_norm\n";

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
		@diff_out = split ' ', `diff_psfm.pl $ref_psfm $runname.psfm $dream`;
		$diff = $diff_out[ 0 ] / $diff_out[ 2 ];
		$diff_total += $diff_out[ 0 ];
		$maxbits_total += $diff_out[ 2 ];
		$nres_total += $diff_out[ 4 ];
		if( $scoretype ne 'byres' ){ `weblogo.pl $runname.spec $nterm \'@diff_out\'`; }
		else{ `weblogo.pl $runname.seq $nterm \'@diff_out\'`; } 
#	push( @pics, "$path"."$runname.png" );
		if( $n_seq_args > 1 ){
			push( @ensemble_psfms, "../$dir/$runname.psfm" );
			if( !`find $home/$all_path -name data.cat.spec` ){
				if( $n_arg == 1 ){
					`awk -F \'qqq\' \'{print \"$dir/\"\$1}\' data.spec > ../$all_dir/data.cat.spec `;
				}
				else{
					`awk -F \'qqq\' \'{print \"$dir/\"\$1}\' data.spec >> ../$all_dir/data.cat.spec `;
				}
			}
		}

#gen and score norm profile
		$runname_norm = $runname.".$bg_tag.$log_norm"."norm";
		$bg_tag = $bg;
		if( $bg ne '-' ){
			if( $bg eq "self" ){
				`gen_pssm.pl data.spec psfm $nterm > data.psfm`;
				`$norm_script data.psfm $runname.psfm > $runname_norm.psfm`;
			}
			elsif( $bg_path ){
				@bg_tags = split '/', $bg;
				$bg_tag = $bg_tags[ $#bg_tags ];
				`$norm_script $bg_path $runname.psfm > $runname_norm.psfm`;
			}
			else{ `$norm_script /home/cking/work/bg/bg_std.psfm $runname.psfm > $runname_norm.psfm`; }
			`gen_seq.pl $runname_norm.psfm 10000 > $runname_norm.seq`;


			@diff_norm_out = split ' ', `diff_psfm.pl $ref_psfm $runname_norm.psfm $dream`;
			$diff_norm = $diff_norm_out[ 0 ] / $diff_norm_out[ 2 ];
			$diff_norm_total += $diff_norm_out[ 0 ];
			$nterm_norm = ( split ' ', `head -n 1 $runname_norm.psfm` )[ 0 ];
			`weblogo.pl $runname_norm.seq $nterm_norm \'@diff_norm_out\'`;
		}
	#	push( @pics_norm, "$path"."$runname_norm.png" );
		if( $bg eq '-' ){ printf "%.3f ", $diff; }
		else{ printf "%.3f ", $diff_norm; }
	#	`cp $runname.png ~/transfer`;
	#	`cp $runname_norm.png ~/transfer`;
		if( $show eq "show" ){
			if( $bg ne '-' ){ $picname = "$runname_norm.png"; }
			else{ $picname = "$runname.png"; }
			system( "display $picname & " );
		}
		chdir "$home";
	}

#ensemble analysis?	
	if( $n_seq_args > 1 ){
		$all_runname = "$protein.$all_dir.$scoretype-$cutoff";
		chdir "$all_path";
		if( `find .  -maxdepth 1 -name $all_runname.psfmlist` ){ `rm $all_runname.psfmlist`;}
		foreach( @ensemble_psfms ){ `echo $_ >> $all_runname.psfmlist`; }
		`add_psfm.pl $all_runname.psfmlist > $all_runname.psfm`;
		`data2logo.pl $all_runname.psfm $ref_psfm $nterm $bg_path $dream`;
#	`cp $all_runname.norm.png ~/transfer`;
		`pep_sort.pl data.cat.spec $cutoff $scoretype > $all_runname.cat.spec`;
		`data2logo.pl $all_runname.cat.spec $ref_psfm $nterm $bg_path $dream`;
		$all_runname_norm = $all_runname.".$bg_tag.$log_norm"."norm";
		`mv $all_runname.norm.png $all_runname_norm.png`;
		`mv $all_runname.cat.norm.png $all_runname_norm.cat.png`;
		if( $show eq "show" || $show eq 'ensemble' ){
			if( $bg ){ $picname = "$all_runname.norm.png"; }
			else{ $picname = "$all_runname.png"; }
			system( "display $picname & " );
			if( $bg ){ $picname = "$all_runname.cat.norm.png"; }
			else{ $picname = "$all_runname.cat.png"; }
			system( "display $picname & " );
		}
	}
	print "\t";
	chdir "$home";
}

$diff_total = $diff_total / $maxbits_total;
$diff_norm_total = $diff_norm_total / $maxbits_total;
if( $bg eq '-' ){ printf "%.3f\n", $diff_total; }
else{ printf "%.3f\n", $diff_norm_total; }

