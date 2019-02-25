#!/usr/bin/perl
if( !$ARGV[ 0 ] ){ die "args:\tsys_filename\tbase.args\tnprocs\t<nametag>\t<partition>\n"; };
$proteins_filename = shift( @ARGV );
$args_base = shift( @ARGV );
$nprocs = shift( @ARGV );
$tag = shift( @ARGV );
if( $tag ){ $tag = $tag."_"; }
$partition = shift( @ARGV ) || "hhigh";

$year = ( split '-', `date --rfc-3339=date` )[ 0 ];
$date = ( split "$year-", `date --rfc-3339=date` )[ 1 ];
chomp( $date );

#input like: superfamily/protein/pdbid.args
@proteins = `cat $proteins_filename`;
chomp( @proteins );
$n_proteins = $#proteins + 1;

$nprocs_per = int( $nprocs / $n_proteins );
$nprocs_extra = $nprocs - $nprocs_per * $n_proteins;

$delete_all = 'n';
foreach $line( @proteins ){
	$line = ( split ' ', $line )[ 0 ];
	@protein_info = split '/', $line;
	$args = pop( @protein_info );
	$protein = ( split "$args", $line )[ 0 ];
	$pdb = ( split '.args', $args )[ 0 ];

	$dir = $tag.$pdb."_".$date;	
	$path = $protein.$dir.'/';

	#ask for overwrite directory
	#ask for overwrite directory
	if( !`find $system  -maxdepth 1 -type d -name $dir` ){
		print "Directory $path does not exists! Skip? (y/n):\t";
		$skip = <STDIN>;
		chomp( $skip );
		if( $skip eq 'y' ){ next; }
		else{ die; }
	}

	`cat $args_base $line > $path/$args`;

	$conf = "resample.conf";
	$args = '@'.$args;
	`( cat $conf; echo \' $args\') | xargs > $path/$conf`;
	$bash = "resample.bash";
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
	chdir "/external2/home/cking/work/";
}

