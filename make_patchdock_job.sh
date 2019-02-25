#!/bin/sh

if [ -z $1 ]; then
  echo "Make a patchdock job"
  echo "USAGE: ~/DockScripts/patchdock/make_patchdock_job.sh < param file1 > < file2 > .."
  exit
fi

until [ -z $1 ]; do
  p=$1
  b=`basename $p | sed 's|.params||'`;
  echo "/work/strauch/patchdock/patch_dock.Linux $b.params output/$b.patchdock"
  shift
done
