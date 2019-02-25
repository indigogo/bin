#!/bin/bash
max_number_of_PDBs=10000
##
/bin/echo "Author: Daniel-Adriano Silva"
/bin/echo "Ver 0.2a, Nov/18/2014"
/bin/echo "THIS SCRIPT IS USED TO PREPARE A \"MASSIVE\" FFF JOB for BOINC"
/bin/echo "IT WORKS ONLY INSIDE OF THE DIGs ENVIROMENT"
/bin/echo "The protocol IS INTENDED FOR TESTING novo-OnlyProtein-desigs. NOT for abinitio prediction of natural proteins!"
/bin/echo "The maximum number of PDB structures admited per job/input is ${max_number_of_PDBs}."
##
#ToDo
##1. Add check for maximum num of pdbs in the list (10K?)
##Add subDirlevels in order to cope with the lame FS! (e.g. 1K max)



#0.Add ctrl-c trap
control_c()
## run if user hits control-c
{
  /bin/echo -en "\n*** You pressed ctr-c. Exiting ***\n"
  exit $?
}
## trap keyboard interrupt (control-c)
trap control_c SIGINT

#1.Global vars
##Increase ulimit to support more "max user processes"
##ulimit -u 5000
##In:
pyRosettaVirtualEnvPath="/work/dadriano/.virtualenvs/my_env/bin/activate"
jobRoot=`pwd`
FFFdir="${jobRoot}/tmp_boincFFF"
parallelBin="/work/dadriano/PROGRAMS/parallel-20141022/bin/parallel"
theFragmentReducerBin="/work/dadriano/Shared/python/FFF/theFragmentReducer_v0.3.py -p 1"
numJobsRelax=3
numJobsAbinitio=5
numParallelJobsFragmentReducer=40
pnodes_file="${jobRoot}/pnodes.txt"
##Fragment Picker stuff
cm_scripts_path="/work/robetta/workspace/labFragPicker_DO_NOT_REMOVE/cm_scripts"
psipred_path="/work/robetta/workspace/labFragPicker_DO_NOT_REMOVE/psipred3.21"
csbuild_path="/work/robetta/workspace/labFragPicker_DO_NOT_REMOVE/csbuild"
boinc_scripts_path="/work/robetta/workspace/labFragPicker_DO_NOT_REMOVE/bakerlab_scripts/boinc"
pnnmake_path="/work/robetta/workspace/labFragPicker_DO_NOT_REMOVE/nnmake"
##Out/then/In
boincJobsFileList="${jobRoot}/tmp_boinc_FFF_jobs_filelist.txt"
##Out for Boinc:
boincJobFile="${jobRoot}/boinc_submitFFFjobs.boinc"
boincJobsNameList="${jobRoot}/boinc_job_names.dat"
failedBuildFragmentsList="${jobRoot}/boinc_jobs_failed_building.txt"
##Extra checks for boinc submission
FFF_boinc_job_submit_log_file_name="${jobRoot}/boinc_job_submit.log"
FFF_boinc_job_id_file_name="${jobRoot}/boinc_job_id.dat"
#Argparse:
inPDBlist=${1}
if  [ ! -f ${inPDBlist} ]
then
	/bin/echo "Input argument 1 (pdbs list): ${inPDBlist} doesn't exist. TERMINATING"
	exit 1
fi
boincSubmitName=${2}
isAGo=${3} 

#2.Source pyrosetta
##source ${pyRosettaVirtualEnvPath}

#3a.Check arguments exist
if [ $# -ne 3 ] 
then
	/bin/echo "ERROR. This program requires exactly 3 arguments. TERMINATING"
	/bin/echo "Argument #1 must be a pdb list with absolute paths"
	/bin/echo "Argument #2 must be a unique BOINC name"
	/bin/echo "Argument #3 must be: \"yes\" (without quotes)"
	exit 1
elif [ ${isAGo} != "yes" ]
then
	/bin/echo "Argument 3 must be: \"yes\" (without quotes)"
	exit 1
fi

#3b.Check tmp Boinc Zip files list doesn't exist
if [ -f ${boincJobsFileList} ]
then
	/bin/echo "BOINC job list: ${boincJobsFileList} exists! Cannot continue (i.e. remove it first). TERMINATING"
	exit 1
fi

#3c Check that the boinc_job_submit.log doesn't exist
if [ -f ${FFF_boinc_job_submit_log_file_name} ]
then
	/bin/echo "BOINC job submission log already exist!!: ${FFF_boinc_job_submit_log_file_name}. Cannot continue. This is likely your mistake! TERMINATING"
	exit 1
fi

#3d Check that the boinc_job_id.dat doesn't exist
if [ -f ${FFF_boinc_job_id_file_name} ]
then
	/bin/echo "BOINC job ID file already exist!!: ${FFF_boinc_job_id_file_name}. Cannot continue. This is likely your mistake! TERMINATING"
	exit 1
fi

#3e. Check that we are not overwriting the jobs_namelist 
if [ -f ${boincJobsNameList}  ]
then
	/bin/echo "boinc subjoblist ${boincJobsNameList} exists an is not empty. Cannot continue (i.e. remove it first). TERMINATING"
fi

#3f. Check that the lenght of the list is not larger than some admited number
if [ `wc -l ${inPDBlist} | awk '{print $1}'` -gt ${max_number_of_PDBs} ]
then
	/bin/echo "ERROR. The maximum numbeer of jobs admited per list is: " ${max_number_of_PDBs}
	/bin/echo "Split your list in multiple jobs. TERMINATING NOW"
	exit 1 
fi

#3g. Check that all the pdb exist
/bin/echo "Checking all PDBs in the input list"
for i in `cat ${inPDBlist}`
do
	if [ ! -f ${i} ]
	then
		/bin/echo "Input ${i} does not exist, Fix it before proceeding any further. TERMINATING program NOW"
		exit 1 
	fi
done
/bin/echo "Done checking PDB list"

#3h. Now make the FFFdir
if [ ! -d ${FFFdir} ]
then
		/bin/echo "Generating ${FFFdir} directory"
		/bin/mkdir ${FFFdir}
		/bin/echo "Done"
elif [ `find  ${FFFdir} | wc -l` -ne 1  ]
then
		/bin/echo "ERROR: ${FFFdir} directory exists an is not empty. Cannot continue (i.e. remove it first). TERMINATING"
		exit 1 
fi


#4.Generate Fragments
#/bin/echo "Generating fragments for all the PDBs using the OLD fragment Database"
#/bin/echo "The general command is /work/robetta/workspace/labFragPicker_DO_NOT_REMOVE/bakerlab_scripts/boinc/make_fragments.py -pdbs_folder ./ -n_proc ${numParallelJobsFragmentPicker}"

#5a.Generate commandlines to reduce the fragments and create the BOINC zip file 
####cd ${FFFdir}
/bin/echo "" > ${boincJobsFileList}
/bin/echo '#!/bin/bash' > ${FFFdir}/parallel_joblist_fragment_reducer.bash
/bin/echo "Now I'll generate the FFF fragment files in parallel, be patient. This uses the old database and DOESN'T consider homology!" 
##for i in `/bin/find ${FFFdir} -maxdepth 1 -type l -o -type f -name '*.pdb'`
/bin/touch ${failedBuildFragmentsList}
for i in `cat ${inPDBlist}`
do
	base_pdb_name=`basename ${i}`
	input_file_path_md5hash=`echo ${i} | /usr/bin/md5sum | tail -n1 | awk '{print \$1}'`
	#This is a trick to avoid generating too many multiple files inside of the same directory
	fragments_dir_name=${FFFdir}/${input_file_path_md5hash:0:2}/${input_file_path_md5hash:0:4}/${input_file_path_md5hash}  ##${FFFdir}/${base_pdb_name/%.pdb/_fragments}
	/bin/echo " \
source ${pyRosettaVirtualEnvPath} && \
/bin/mkdir -p ${fragments_dir_name} && \
cd ${fragments_dir_name} && \
/bin/echo \${hostname} > FFF_fragments.log && \
/bin/cp ${i} ./fff_${base_pdb_name} >> FFF_fragments.log && \
/bin/ln -s ./fff_${base_pdb_name} ./00001.pdb >> FFF_fragments.log && \
${cm_scripts_path}/bin/pdb2fasta.py 00001.pdb > 00001.fasta && \
${psipred_path}/runpsipred_single 00001.fasta >> FFF_fragments.log && \
/bin/ln -s 00001.ss2 00001.psipred_ss2 >> FFF_fragments.log && \
${csbuild_path}/csbuild -i 00001.fasta -I fas -D ${csbuild_path}/csblast-2.2.3/data/K4000.crf -o 00001.check -O chk >> FFF_fragments.log && \
${boinc_scripts_path}/make_checkpoint.pl -id 00001 00001.fasta >> FFF_fragments.log && \
/bin/ln -s ${boinc_scripts_path}/path_defs.txt ./ >> FFF_fragments.log && \
${pnnmake_path}/pNNMAKE.gnu aa 0000 1 &>> FFF_fragments.log && \
/bin/mv aa0000103_05.200_v1_3 00001.200.3mers >> FFF_fragments.log && \
/bin/mv aa0000109_05.200_v1_3 00001.200.9mers >> FFF_fragments.log && \
/bin/rm ./00001.check >> FFF_fragments.log && \
/bin/rm ./00001.checkpoint  >> FFF_fragments.log && \
/bin/rm ./00001.horiz >> FFF_fragments.log && \
/bin/rm ./00001.ss >> FFF_fragments.log && \
/bin/rm ./00001.psipred_ss2 >> FFF_fragments.log && \
/bin/rm ./names.200_v1_3aa00001 >> FFF_fragments.log && \
/bin/rm ./path_defs.txt >> FFF_fragments.log && \
if [ -f \"./00001.200.3mers\" ] && [ -f \"./00001.200.3mers\" ] && [ -f \"./00001.pdb\" ]; \
then \
 /work/dadriano/.virtualenvs/my_env/bin/python ${theFragmentReducerBin} >> FFF_fragments.log && \
 /bin/rm 00001.200.3mers >> FFF_fragments.log && \
 /bin/rm 00001.200.9mers >> FFF_fragments.log && \
 pdbmd5=\`/usr/bin/md5sum ./00001.pdb | tail -n1 | awk '{print \$1}'\` && \
 fdate=\`/bin/date\` && \
 fdate=\${fdate// /_} && \
 fdate=\${fdate//:/_} && \
 boincJobFileName=FFF_${input_file_path_md5hash}_${boincSubmitName}_\${fdate} && \
 /usr/bin/zip \${boincJobFileName}  00001.pdb 00001.3.3mers 00001.3.9mers >> FFF_fragments.log && \
 /bin/echo \"\${PWD}/\${boincJobFileName}.zip\" >> ${boincJobsFileList} && \
 /bin/echo ${i} ${base_pdb_name} > \${boincJobFileName}.info && \
 /bin/ln -s 00001.fasta \${boincJobFileName}.fasta >> FFF_fragments.log; \
else \
 /bin/echo \"Missing fragment files for: ${i}. Cannot continue, writting to: ${failedBuildFragmentsList}\" \
 /bin/echo ${i} >> ${failedBuildFragmentsList} \
 exit 1; \
fi " >> ${FFFdir}/parallel_joblist_fragment_reducer.bash
done

#5b.Execute 3a in parallel
cd ${FFFdir}
if [ -f ${pnodes_file} ]
then
	num_pnodes=`wc -l ${pnodes_file} | awk '{print $1}'`
	/bin/echo "Generating fragments and boinc jobs using ${num_pnodes} parallel nodes with the file: ${pnodes_file} (${numParallelJobsFragmentReducer} threads/node)"
	/bin/echo "Total number of threads: " `expr ${numParallelJobsFragmentReducer} \* ${num_pnodes}`
	/bin/echo "Nodes address list: " 
	/bin/cat ${pnodes_file}
	${parallelBin} --jobs ${numParallelJobsFragmentReducer} --sshloginfile ${pnodes_file} --workdir ${FFFdir} --no-notice --bar < parallel_joblist_fragment_reducer.bash
else
	echo "Generating fragments and boinc jobs using only the localhost (${numParallelJobsFragmentReducer} parallel threads)"
	${parallelBin} -j ${numParallelJobsFragmentReducer} --no-notice --bar < parallel_joblist_fragment_reducer.bash
fi
/bin/echo "AllDone"

#5c Check if any job failed
num_failed_fragment_jobs=`/usr/bin/wc -l ${failedBuildFragmentsList} | awk '{print $1}'`
if [ ${num_failed_fragment_jobs} -eq 0 ];
then 
	echo "ALL fragments have been generated sucesfully!"
	/bin/rm ${failedBuildFragmentsList}
else
	echo -e "WARNING: the generation of fragments for ${num_failed_fragment_jobs} of the input PDBs have FAILED. \
 For more details check the file: \n ${failedBuildFragmentsList} \n "
fi

#6. Generate BOINC job
###Return to the jobRoot
cd ${jobRoot}
/bin/echo "Fasten your Seat Belt! Finally I'll generate the BOINC Jobs! "
/bin/echo "application = minirosetta" > ${boincJobFile}
/bin/touch ${boincJobsNameList}
counter=1
for i in `cat ${boincJobsFileList}`
do
	if [ -f ${i} ]
	then
		counter_f=`printf "%07d" ${counter}`
		
		thisFilename=`echo ${i} |sed 's/\// /g'| awk '{print $(NF)}'`
		general_job_name="${thisFilename/%.zip/}_${counter_f}"
		general_job_fasta_seq=`cat ${i/%.zip/.fasta} | grep -v '>' | awk 'START{lineout=""}{lineout=lineout $1}END{print lineout}'`
		general_job_info=`cat ${i/%.zip/.info} | awk '{print $1 " " $2}'`
		abinitio_job_name="${general_job_name}_abinitio_SAVE_ALL_OUT"
		relax_job_name="${general_job_name}_relax_SAVE_ALL_OUT"
		echo "${general_job_name} ${general_job_fasta_seq} ${general_job_info}" >> ${boincJobsNameList}
		
		/bin/echo "##ABINITIO  FFF_${boincSubmitName}_${counter_f}_abinitio ${i}"
		/bin/echo "name = ${abinitio_job_name}"
		/bin/echo "description = abinitio fold design structure (${abinitio_job_name})"
		/bin/echo "inputfiles = ${i}"
		/bin/echo "arguments = \
-abinitio::fastrelax \
-database minirosetta_database \
-ex1 \
-ex2aro \
-in:file:boinc_wu_zip ${thisFilename} \
-in:file:native 00001.pdb \
-in:file:fullatom \
-frag3 00001.3.3mers \
-frag9 00001.3.9mers \
-abinitio::number_3mer_frags 3 \
-abinitio::number_9mer_frags 3 \
-abinitio::increase_cycles 5 
-abinitio::detect_disulfide_before_relax \
-abinitio::use_filters false \
-relax::default_repeats 5 \
-out:file:silent default.out \
-out:file:silent_struct_type score \
-silent_gz \
-mute all "
		/bin/echo "resultfiles = default.out.gz"
		/bin/echo "queue = ${numJobsAbinitio}"
		/bin/echo "##ABINITIO END"
		
		/bin/echo "##RELAX  FFF_${boincSubmitName}_${counter_f}_abinitio ${i}"
		/bin/echo "name = ${relax_job_name}"
		/bin/echo "description = relax design structure (${relax_job_name})"
		/bin/echo "inputfiles = ${i}"
		/bin/echo "arguments = \
-run:protocol relax \
-database minirosetta_database \
-ex1 \
-ex2aro \
-in:file:boinc_wu_zip ${thisFilename} \
-in:file:s 00001.pdb \
-in:file:native 00001.pdb \
-in:file:fullatom \
-relax::default_repeats 15 \
-out:file:silent default.out \
-out:file:silent_struct_type score \
-silent_gz \
-mute all"
		/bin/echo "resultfiles = default.out.gz"
		/bin/echo "queue = ${numJobsRelax}"
		/bin/echo -e "##RELAX END\n"
		#Increase the job counter
		let counter+=1
	else
		/bin/echo "Sadly Boinc File: ${i} is missing! This shouldn't be happening. Maybe you ran out of space?. TERMINATING"
		echo "#FAILED" > ${boincJobsNameList}
		#Do not use this list if something is wrong
		echo "#FAILED" > ${boincJobsNameList}
		rm ${boincJobsNameList}
		echo "#FAILED" > ${boincJobFile}
		rm ${boincJobFile}
		exit 1
	fi
done >> ${boincJobFile}


#7.Clean buildFiles
##7.1 Remove the tmp boincJobsFileList
rm ${boincJobsFileList}
#7.2 Remove the fragments and other files !!!!Be super carefull with this rm -Rf!!! 
####rm -Rf ${FFFdir} #THIS IS DISABLED: I think this should be done by the user itself!

#8. Give some feedback to Jhon D
/bin/echo "Boinc Job Preparation Finished; \"IF\" all is right submit it using:" 
/bin/echo "  #>  /work/dadriano/DEVEL/boincFFF/BASH/submit_boinc_FFF_job.bash  yes"
/bin/echo "Bye"





