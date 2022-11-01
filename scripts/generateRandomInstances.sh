#!/bin/bash

set -o errexit

if [[ "$#" != "5" ]]; then
	echo "Usage: bash generateRandomInstances.sh [instances] [rooms] [classes] [times] [students]"
	exit 0
fi

echo -e "k\tr\tc\tt\ts"
echo -e "$1\t$2\t$3\t$4\t$5" 

DIR="k$1r$2c$3t$4s$5"
mkdir $DIR

for ((i = 0 ; i < $1 ; i++)); do
  echo "Generating instance $i"
  perl make_random_input.pl $2 $3 $4 $5 "k$1r$2c$3t$4s$5/constraints_$i" "k$1r$2c$3t$4s$5/prefs_$i" 
done

