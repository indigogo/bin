#!/bin/bash

#for every file in cwd that matched *_fold_*.out
for fold in $(ls *_fold_*.out.bz2)
do
	#create a new variable that copies $fold and then replaces "_fold_" with "_relax_"
	relax=`echo $fold | sed 's/_fold_/_relax_/'`
	#rm prev version of tmp file
	rm nrg.gplt
	#create new tmp file that hold gnuplot commands
	echo "set autoscale" >> nrg.gplt
	echo "set terminal png" >> nrg.gplt
	echo "set output \"$fold.png\"" >> nrg.gplt
	echo "plot \"<sd.py $relax\", \"<sd.py $fold\"" >> nrg.gplt
	#run gnuplot, pipe in tmp file
	gnuplot < nrg.gplt
done
