#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tsys_filename\tbase.args\tnprocs\t<nametag>\t<partition>\t<n_seq_args>\n"; };
$proteins_filename = shift( @ARGV );
$args_base = shift( @ARGV );
$nprocs = shift( @ARGV );
$tag = shift( @ARGV );
if( $tag ){ $tag = $tag."."; }
$partition = shift( @ARGV ) || "hhigh";
$n_seq_args = shift( @ARGV ) || 1;

$year = ( split '-', `date --rfc-3339=date` )[ 0 ];
$date = ( split "$year-", `date --rfc-3339=date` )[ 1 ];
chomp( $date );

#input like: superfamily/protein/pdbid.args
@proteins = `cat $proteins_filename`;
chomp( @proteins );
$n_proteins = $#proteins + 1;
$n_proteins = $n_proteins * $n_seq_args;

$nprocs_per = int( $nprocs / $n_proteins );
$nprocs_extra = $nprocs - $nprocs_per * $n_proteins;
$home = `pwd`;
chomp( $home );

$delete_all = 'n';
foreach $line( @proteins ){
	$line = ( split ' ', $line )[ 0 ];
	@protein_info = split '/', $line;
	$args = pop( @protein_info );
	$protein = ( split "$args", $line )[ 0 ];
	$pdb = ( split '.args', $args )[ 0 ];

	foreach $n_arg( 1..$n_seq_args ){

		$dir = $tag.$pdb.".".$date;	
		if( $n_seq_args > 1 ){ $dir = $tag.$pdb.".".$n_arg.".".$date; }
		$path = $protein.$dir.'/';

		#ask for overwrite directory
		if( `find $protein -maxdepth 1 -type d -name $dir` ){
			if( $delete_all eq 'all' ){ `rm -rf $path` }
			else{
				print "Directory $path exists! Overwrite? (y/n/all):\t";
				$delete = <STDIN>;
				chomp( $delete );
				if( $delete eq 'y' ){ `rm -rf $path`; }
				elsif( $delete eq 'all' ){
					`rm -rf $path`;
					$delete_all = $delete;
				}
				else{ next; }
			}
		}
		`mkdir $path`;

		`cat $args_base $line > $path/$args`;
		if( $n_seq_args > 1 ){ `sed s/=/$n_arg/ $path/$args > $path/$args.tmp; mv $path/$args.tmp $path/$args`; }

		$conf = "spec.conf";
		`( cat $conf; echo \' \@$args\') | xargs > $path/spec.conf`;
		$bash = "spec.bash";
		`sed s/partition/$partition/ $bash > $path/$bash`;

		chdir "$path";
		`chmod a+x $bash`;
		$my_nprocs = $nprocs_per;
		if( $nprocs_extra > 0 ){
			$my_nprocs = $my_nprocs + 1;
			$nprocs_extra = $nprocs_extra - 1;
		}
		print "Running $path on $my_nprocs procs...\n";

		`./$bash $my_nprocs`;
		chdir "$home";
	}
}

