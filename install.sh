#!/bin/sh

julia_install(){
  echo "Installing julia interface"
  julia -e "using Pkg; Pkg.develop(path=\"$pkg/julia/LasapInterface\")"
}

pkg=$(dirname "$0")

pip install --user --break-system-packages $pkg || pip install --user $pkg

cp $pkg/scripts/* $HOME/.local/bin #2>/dev/null TODO: find a better solution for this

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
