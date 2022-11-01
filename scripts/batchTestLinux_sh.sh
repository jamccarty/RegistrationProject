#!/bin/bash

CONSTRAINTS_PREFIX="constraints_"
PREFS_PREFIX="prefs_"

set -o errexit

if [[ "$#" != "2" ]]; then
	echo "Usage: bash batchTest.sh [dirname] [scriptdirname]"
	echo "Dirname should contain subfolders, each of which contains prefs and constraints files"
	echo "Scriptname should be relative path to a folder containing a run.sh"
	exit 0
fi

ORIGINAL=`pwd`
echo $ORIGINAL

# Go to directory 
cd $1

echo "directory, avg time, avg fit"

# Process each subdirectory 
for directory in `find . -maxdepth 1 -mindepth 1 -type d`
do
	# Enter subdirectory 
	#echo examining $directory 
	cd $directory
	current=`pwd`

	# How many pairs are in here 
	# We assume pairs are named 
		# constraints_i
		# preferences_i 
	NUM_FILES=`find . -type f -name "constraints_*"| wc -w`
	#echo $NUM_FILES
	TOTAL_TIME=0
	TOTAL_FIT=0
	for ((i = 0 ; i < NUM_FILES ; i++)); do
		
		# Get filenames 
		CONSTRAINTS_FILE="$current/$CONSTRAINTS_PREFIX$i"
		PREFS_FILE="$current/$PREFS_PREFIX$i"


		start_time=$(date +%s.%3N)
		# Run script on them
		result=`(cd $ORIGINAL/$2; bash run.sh $CONSTRAINTS_FILE $PREFS_FILE $current/output$i.txt | tail -n 1)`
		#result=`(echo $result > tail -n 1)`
		end_time=$(date +%s.%3N)

		# elapsed time with millisecond resolution
		# keep three digits after floating point.
		elapsed=$(echo "scale=3; ($end_time - $start_time)*1000" | bc)
		#echo $elapsed $result

		#echo $INSTANCE_TIME
		TOTAL_FIT=$(echo "scale=3; ($TOTAL_FIT + $result)" | bc)
		TOTAL_TIME=$(echo "scale=3; ($TOTAL_TIME + $elapsed)" | bc)
		#TOTAL_TIME=$(( $TOTAL_TIME + $elapsed ))

	done 
	time=`bc <<<"scale=2; $TOTAL_TIME / 10"`
	fit=`bc <<<"scale=3;$TOTAL_FIT / 10"`
	echo "$directory, $time, $fit"
	
	cd ..
done
