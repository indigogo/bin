#!/bin/bash
#cant have '.' in submit name!
#if (( $# != 1 ))
#then
#        echo "args:  jobname  fasta_input"
#        exit
#fi

/work/chrisk/bin/robetta_submit.py --registered_email cmiles@u.washington.edu --reply_email chrisk1@u.washington.edu  --name $1 --fasta $2
echo "\n\n--!!-- goto http://robetta.bakerlab.org/queue.jsp and search for target name in Target search field --!!--\n"
