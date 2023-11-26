#!/bin/bash 

# Running Instructions:
#   $ chmod +x ./benchmark_rev.sh
#   $ time ./benchmark_rev.sh

# $1 :: agent name
# $2 :: timeout
# $3 :: start move (higher)
# $4 :: end move

if [ -z ${1+x} ] || [ -z ${2+x} ] || [ -z ${3+x} ] ||  [ -z ${4+x} ]
then 
  echo "usage :: ./benchmark_rev.sh <agent> <timeout> <start-move> <end-move>"
else
  count=0
  for moves in $( seq $3 -1 $4 )
  do
    echo "==== ${1} playing at ${moves} moves ===="
    time python3 benchmark_rev.py $1 $moves $2 debug=False
    echo "========================================"
  done
fi

# run benchmark minim
# run benchmark alpha
# run benchmark omega
# run benchmark fhourstone
# print stats