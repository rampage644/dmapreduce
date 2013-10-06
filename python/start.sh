#!/bin/bash
source ./run.env

rm data/*.dat -f
rm log/* -f

ZVM_REPORT=report.txt

#config for mapreduce network
MAP_FIRST=1
MAP_LAST=4
REDUCE_FIRST=1
REDUCE_LAST=4

#calculate number of nodes for whole cluster
let NUMBER_OF_NODES=${MAP_LAST}+${REDUCE_LAST}

./ns_start.sh ${NUMBER_OF_NODES}

rm ${ZVM_REPORT} -f
time

COUNTER=$MAP_FIRST
while [  $COUNTER -le $MAP_LAST ]; do
    echo ${SETARCH} ${ZEROVM} -Mmanifest/map$COUNTER.manifest
    ${SETARCH} ${ZEROVM} -PQs -Mmanifest/map$COUNTER.manifest >> ${ZVM_REPORT} &
    let COUNTER=COUNTER+1 
done

COUNTER=$REDUCE_FIRST
#run reduce nodes -1 count
while [  $COUNTER -lt $REDUCE_LAST ]; do
    echo ${SETARCH} ${ZEROVM} -Mmanifest/reduce$COUNTER.manifest
    ${SETARCH} ${ZEROVM} -PQs -Mmanifest/reduce$COUNTER.manifest >> ${ZVM_REPORT} &
    let COUNTER=COUNTER+1 
done

#run last reduce node
echo /usr/bin/time ${SETARCH} ${ZEROVM} -PQs -Mmanifest/reduce"$REDUCE_LAST".manifest
${SETARCH} ${ZEROVM} -PQs -Mmanifest/reduce"$REDUCE_LAST".manifest >> ${ZVM_REPORT} 

#zgdb reduce.manifest
#zgdb map.manifest


./ns_stop.sh

for job in `jobs -p`
do
    wait $job
done

cat ${ZVM_REPORT}

#test results
rm data/temp.sum -f
COUNTER=1
while [  $COUNTER -le $REDUCE_LAST ]; do
    ./valsort -t4 -o data/"$COUNTER"result.sum data/"$COUNTER"sorted.dat
    cat data/"$COUNTER"result.sum >> data/temp.sum
    let COUNTER=COUNTER+1 
done
#./gensort-1.5/valsort -s data/temp.sum > data/out.sum
#diff data/in.sum data/out.sum
