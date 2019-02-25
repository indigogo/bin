#!/usr/bin/perl
if( $#ARGV < 2 ){ die "args:\tseq_list\targs_template\tcpus_per_seq\n"; }
$listname = shift( @ARGV );
$argsname = shift( @ARGV );
$n_nodes = shift( @ARGV );

@list = `cat $listname`;
foreach $line( @list ){
	$name = ( split ' ', $line )[ 0 ];
	$seq = ( split ' ', $line )[ 1 ];
	`mkdir $name`;
	`(cat $argsname; echo -pep_spec::input_seq $seq; echo -o $name) > $name/args`;
	$pdbname = "$name.%t";
	`(cat args.conf; echo -o $pdbname) | xargs > $name/args.conf`;
	`cp run_job.bash $name;`;
	`cd $name; ./run_job.bash $name $n_nodes; cd ..`;
}
