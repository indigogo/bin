#!/bin/sh

if [ $# -lt 3 ]; then
  echo "Creates parameter files for patchdock runs. The output will be contained in a dir. tree."
  echo "USAGE: ~/DockPatch/Scripts/make_PatchDock_params.sh < Binders.list > <Targets.list > < output dir> <[KNOB]>"
  echo "KNOB is optional and is only used if a the receptor (aka Binder) is presending a KNOB, rather than the default HOLE. Stating ALL will produce hole/knob/flat for both"
  exit 1;
fi

Binders=$1
Targets=$2
output_dir=$3
receptor_type=$4

for b in `cat $Binders`; do
  b_4let=`basename $b | awk -F . '{print $1}'`
  mkdir -p $output_dir/$b_4let;
  for t in `cat $Targets`; do
    t_4let=`basename $t | awk -F . '{print $1}'`
    echo $b_4let"_"$t_4let
    ~sarelf/PatchDock/buildParams.pl $b $t 4.0 EI
	 new_name="${b_4let}_${t_4let}.params";
	 mv params.txt $new_name
	 ~sarelf/DockScripts/patchdock/adjust_PatchDock_params.sh $new_name $receptor_type
	 mv $new_name $output_dir/$b_4let/;
  done
done
