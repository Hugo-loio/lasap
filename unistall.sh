#!/bin/sh

pkg=$(dirname "$0")

pip uninstall --break-system-packages lasap

if [ ! -z "$(which julia)" ] ; then
  pkgs=$(julia -e "using Pkg; Pkg.status()")
  [ -z $(echo $pkgs | grep "LasapInterface") ] || 
    julia -e "using Pkg; Pkg.rm(\"LasapInterface\")"
fi
