#!/bin/bash
max_number_of_PDBs=10000
##
/bin/echo "Author: Daniel-Adriano Silva"
/bin/echo "Ver 0.2.1a, Dec/18/2014, update chrisk more lenient cutoff values for pass/fail"
/bin/echo "THIS SCRIPT IS USED TO ANALYZE A \"MASSIVE\" FFF JOB for BOINC"
/bin/echo "IT WORKS ONLY INSIDE OF THE DIGs ENVIROMENT"

#0.Add ctrl-c trap
control_c()
## run if user hits control-c
{
  /bin/echo -en "\n*** You pressed ctr-c. Exiting ***\n"
  exit $?
}
## trap keyboard interrupt (control-c)
trap control_c SIGINT

pyRosettaVirtualEnvPath="/work/dadriano/.virtualenvs/my_env/bin/activate"
#2.Source pyrosetta
source ${pyRosettaVirtualEnvPath}

python /work/chrisk/bin/fff/analysis_uFFF.py
