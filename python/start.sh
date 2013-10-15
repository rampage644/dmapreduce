#!/bin/bash
ZEROVM="${ZVM_PREFIX}/bin/zerovm -QPs"

rm data/*.dat -f
rm log/* -f

ZVM_REPORT=report.txt

if [ $# -lt 1 ]
    then
    echo "usage: gendatamanifest.sh <dirname>"
    echo "Example: gendatamanifest.sh terasort"
    exit 1
fi

DIRNAME=$1

#config for mapreduce network
MAP_FIRST=1
MAP_LAST=4
REDUCE_FIRST=1
REDUCE_LAST=4

#calculate number of nodes for whole cluster
let NUMBER_OF_NODES=${MAP_LAST}+${REDUCE_LAST}

./ns_start.sh ${NUMBER_OF_NODES}

rm ${ZVM_REPORT} -f $DIRNAME/*.nexe $DIRNAME/*.tar
rm $DIRNAME/log/ -rf
mkdir $DIRNAME/log
ln -s `pwd`/python.nexe $DIRNAME/
ln -s `pwd`/python.tar $DIRNAME/

COUNTER=$MAP_FIRST
while [  $COUNTER -le $MAP_LAST ]; do
    echo ${SETARCH} ${ZEROVM} $DIRNAME/manifest/map$COUNTER.manifest
    ${SETARCH} ${ZEROVM} $DIRNAME/manifest/map$COUNTER.manifest >> ${ZVM_REPORT} &
    let COUNTER=COUNTER+1 
done

COUNTER=$REDUCE_FIRST
#run reduce nodes -1 count
while [  $COUNTER -le $REDUCE_LAST ]; do
    echo ${SETARCH} ${ZEROVM} $DIRNAME/manifest/reduce$COUNTER.manifest
    ${SETARCH} ${ZEROVM} $DIRNAME/manifest/reduce$COUNTER.manifest >> ${ZVM_REPORT} &
    let COUNTER=COUNTER+1 
done

#zgdb reduce.manifest

for job in `jobs -p`
do
    wait $job
done

./ns_stop.sh

cat ${ZVM_REPORT}
