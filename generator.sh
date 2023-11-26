#!/bin/bash 

# Running Instructions:
#   $ chmod +x ./generator.sh
#   $ time ./genrator.sh

function file_name {
  if [ $(expr $1 / 10) -gt 0 ]
    then
      echo "${1}${2}"
    else
      echo "0${1}${2}"
  fi
}

count=0
for back_move in {1..10} # TODO :: get last back_move from shell
do
  for num_tests in $(seq 5 5 50)
  do
    file_iden=$(file_name $back_move $(expr $(expr $num_tests / 5) - 1))
    python3 generator.py $num_tests $back_move $file_iden
    count=$(expr $count + 1)
    # echo "${count} :: ${file_iden} (${back_move},${num_tests})"
  done
done

echo "run \`generator.py\` ${count} times"
echo " upto ${back_move} moves back"

# run benchmark minim
# run benchmark alpha
# run benchmark omega
# run benchmark fhourstone
# print stats