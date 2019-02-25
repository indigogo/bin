#!/bin/sh

if [ $# -lt 1 ]; then
  echo "sets up a dockpatch run on the non-syd clusters"
  echo "USAGE: setup_clusters_for_PatchDock.sh \$clusters"
  exit 1;
fi

until [ -z $1 ]; do
  c=$1
  cat header > PatchDock_params/job.$c; 
  awk '{print "arguments = "$1,"outputfiles/"substr($1,1,15)".out"; print "queue 1"}' PatchDock_params/params.list.$c >> PatchDock_params/job.$c; 

  ssh $c rm -rf /users/sarelf/Runs/PatchDock
  ssh $c mkdir -p /users/sarelf/Runs/PatchDock/Params /users/sarelf/Runs/PatchDock/Binders/ppk /users/sarelf/Runs/PatchDock/Targets/ppk /users/sarelf/Runs/PatchDock/Constraints /users/sarelf/Runs/PatchDock/outerr; 
	rsync -avzr PatchDock_params/???? $c:/users/sarelf/Runs/PatchDock/ ;  
	rsync -azvr PatchDock_params/job.$c $c:/users/sarelf/Runs/PatchDock/; 
	rsync -avzr ~/PatchDock/patch_dock.Linux $c:/users/sarelf/bin/; 
	rsync -azvr ~/PatchDock/chem.lib $c:/users/sarelf/bin/; 
#   rsync -azvr ../Binders/ppk/* $c:/users/sarelf/Runs/PatchDock/Binders/ppk/; 
#	rsync -azvr ../Targets/ppk/* $c:/users/sarelf/Runs/PatchDock/Targets/ppk/; 
   rsync -azvr Dataset/Binders/ppk/* $c:/users/sarelf/Runs/PatchDock/Binders/ppk/; 
	rsync -azvr Dataset/Targets/ppk/* $c:/users/sarelf/Runs/PatchDock/Targets/ppk/; 
   rsync -avzr Dataset/Constraints $c:/users/sarelf/Runs/PatchDock/;
	rsync -avzr DIR_STRCT/???? $c:/users/sarelf/Runs/PatchDock/outputfiles/

   shift
done
