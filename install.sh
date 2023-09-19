#!/bin/sh

julia_dependencies(){
  echo "Checking dependencies..."
  dependencies="DataFrames OrderedCollections"
  pkgs=$(julia -e "using Pkg; Pkg.status()")

  for dependency in $dependencies ; do
    if [ -z $(echo $pkgs | sed 's/\ /\n/g' | grep $dependency) ] ; then
      echo "Installing" $dependency".jl"
      julia -e "using Pkg; Pkg.add(\"$dependency\")"
    fi
  done
}

julia_install(){
  echo "Installing julia interface"
  #julia_dependencies
  julia -e "using Pkg; Pkg.develop(path=\"$pkg/julia/LasapInterface\")"
}

pkg=$(dirname "$0")

pip install --user --break-system-packages $pkg

cp $pkg/scripts/lasap_merge_daemon $HOME/.local/bin/lasap_merge_daemon

#exit

langs="julia dummy"

echo "\nChoose languages to install interfaces:"
i=1
for lang in $langs ; do
  echo $i"-"$lang
  i=$((i+1))
done
echo "(eg \"1 2\")"
read answer
for number in $answer ; do
  lang=$(echo $langs | cut -d " " -f $number)
  if [ ! -z $lang ] ; then
    case $lang in
      "julia")
	julia_install
	;;
    esac
  else
    echo \"$number\" "is not a valid answer"
  fi
done
