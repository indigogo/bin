#!/bin/sh

if [ $# -lt 1 ]; then
  echo "adjusts the default params.txt output from PatchDock's buildParams to point to the directory"
  echo "placement Binders/ppk, Targets/ppk and Constraints/"
  echo "Also allows the user to specify if the receptor is a KNOB, rather than a HOLE. Stating ALL produces all combinations of possibilities, holes/flat/knob for both receptor and binder"
  echo "USAGE: adjust_PatchDock_params.sh params.txt [KNOB]"
  exit 1;
fi

params=$1
receptor_type=$2

ligand_name=`basename $params | sed 's|_| |' | sed 's|\.| |' | awk '{print $2}'`
receptor_name=`basename $params | sed 's|_| |' | awk '{print $1}'`
awk 'NR<6' $params > params.TMP
b=`awk 'NR==6{print $2}' $params ` # | sed 's|ppk\.||'`
bname=`basename $b`;
awk 'NR==6{print $1,"Binders/ppk/'$bname'"}' $params >> params.TMP
b=`awk 'NR==7{print $2}' $params ` # | sed 's|ppk\.||'`
bname=`basename $b`;
awk 'NR==7{print $1,"Targets/ppk/'$bname'"}' $params >> params.TMP
b=`awk 'NR==8{print $2}' $params`
bname=`basename $b`;
awk 'NR==8{print $1,"Binders/ppk/'$bname'"}' $params >> params.TMP
b=`awk 'NR==9{print $2}' $params`
bname=`basename $b`;
awk 'NR==9{print $1,"Targets/ppk/'$bname'"}' $params >> params.TMP
echo "receptorActiveSite Constraints/$receptor_name.constraints" >> params.TMP
awk 'NR==11' $params >> params.TMP
echo "protLib /work/strauch/patchdock/chem.lib" >> params.TMP
awk '(NR>12) && (NR<33)' $params >> params.TMP
if [ "$receptor_type" == "KNOB" ]; then
	echo "receptorSeg 10.0 20.0 1.5 1 0 0 3" >> params.TMP
	echo "ligandSeg 10.0 20.0 1.5 0 0 1 4" >> params.TMP
elif [ "$receptor_type" == "ALL" ]; then
	echo "receptorSeg 10.0 20.0 1.5 1 1 1 3" >> params.TMP
	echo "ligandSeg 10.0 20.0 1.5 1 1 1 4" >> params.TMP
else
	echo "receptorSeg 10.0 20.0 1.5 0 0 1 3" >> params.TMP
  echo "ligandSeg 10.0 20.0 1.5 1 0 0 4" >> params.TMP
fi

awk 'NR>34' $params >> params.TMP

mv params.TMP $params
