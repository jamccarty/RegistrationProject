#!/bin/bash

set -o errexit

if [[ "$#" != "6" ]]; then
	echo "Usage: bash generateRandomInstances.sh [instances] [rooms] [classes] [times] [students] [majors]"
	exit 0
fi

echo -e "k\tr\tc\tt\ts\tm"
echo -e "$1\t$2\t$3\t$4\t$5\t$6" 

DIR="k$1r$2c$3t$4s$5m$6"
mkdir $DIR

for ((i = 0 ; i < $1 ; i++)); do
  echo "Generating instance $i"
  # perl make_random_input.pl $2 $3 $4 $5 $6 "k$1r$2c$3t$4s$5m$6/jac_scripts/js$5/js$3-$5/constraints_$i" "k$1r$2c$3t$4s$5m$6/prefs_$i" 
    perl make_random_input.pl $2 $3 $4 $5 $6 "k$1r$2c$3t$4s$5m$6/constraints_$i" "k$1r$2c$3t$4s$5m$6/prefs_$i" 

done

