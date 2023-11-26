#!/bin/bash 

# Running Instructions:
#   $ chmod +x ./generator_rev.sh
#   $ time ./genrator_rev.sh

# difference :: all tests are exactly $back_move behind full board

function file_name {
  if [ $(expr $1 / 10) -gt 0 ]
    then
      echo "${1}${2}"
    else
      echo "0${1}${2}"
  fi
}

count=0
for moves in {1..40} # TODO :: get last back_move from shell
do
  for num_tests in $(seq 5 5 50)
  do
    file_iden=$(file_name $moves $(expr $(expr $num_tests / 5) - 1))
    python3 generator_rev.py $num_tests $moves $file_iden
    count=$(expr $count + 1)
    echo "${count} :: ${file_iden} (${moves},${num_tests})"
  done
done

echo "run \`generator2.py\` ${count} times"
echo " upto ${moves} moves"

# run benchmark minim
# run benchmark alpha
# run benchmark omega
# run benchmark fhourstone
# print stats