#!/bin/sh

julia_install(){
  echo "\nInstalling the julia interface..."
  julia -e "using Pkg; Pkg.develop(path=\"$pkg/julia/LasapInterface\")"
}

cpp_install(){
  echo "\nInstalling the C++ interface..."
  build_dir="$pkg/CPP/LasapInterface/build"
  [ -d $build_dir ] || mkdir $build_dir
  cd $build_dir
  cmake .. 
  make
  make install
}

pkg=$(dirname $(realpath "$0"))

pip install --user --break-system-packages $pkg || pip install --user $pkg

cp $pkg/scripts/* $HOME/.local/bin #2>/dev/null TODO: find a better solution for this

langs="julia c++"

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
      "c++")
	cpp_install
	;;
    esac
  else
    echo \"$number\" "is not a valid answer"
  fi
done
