#!/bin/bash

SCRIPT=$(readlink -f "$0")
SCRIPT_PATH=`dirname "$SCRIPT"`

if [ $# -lt 1 ]
    then
    echo "usage: gendatamanifest.sh <dirname>"
    echo "Example: gendatamanifest.sh terasort"
    exit 1
fi

DIRNAME=$1

#Generate from template
MAP_FIRST=1
MAP_LAST=4
REDUCE_FIRST=1
REDUCE_LAST=4

DATA_OFFSET=0
SEQUENTIAL_ID=1

#do relace and delete self communication map channels
COUNTER=$MAP_FIRST
while [  $COUNTER -le $MAP_LAST ]; do
#genmanifest
    NAME=map \
    TIMEOUT=500 \
    NODEID=$COUNTER \
    ABS_PATH=$SCRIPT_PATH/$DIRNAME \
    CHANNELS_INCLUDE=$DIRNAME/manifest/map.channels.manifest.include \
    SEQUENTIAL_ID=$SEQUENTIAL_ID \
    ./template.sh $DIRNAME/manifest/manifest.template | \
    sed /map"$COUNTER"-map-"$COUNTER"/d | \
    sed s@w_map"$COUNTER"-@/dev/out/@g | \
    sed s@r_map"$COUNTER"-@/dev/in/@g > $DIRNAME/manifest/map"$COUNTER".manifest 
#gennvram
    NODEID=$COUNTER \
    ./template.sh $DIRNAME/nvram/map.nvram.template > $DIRNAME/nvram/map"$COUNTER".nvram

    let SEQUENTIAL_ID=SEQUENTIAL_ID+1
    let COUNTER=COUNTER+1 
    let DATA_OFFSET=DATA_OFFSET+SINGLE_NODE_INPUT_RECORDS_COUNT
done

COUNTER=$REDUCE_FIRST
while [  $COUNTER -le $REDUCE_LAST ]; do
#genmanifest
    NAME=reduce \
    TIMEOUT=500 \
    NODEID=$COUNTER \
    ABS_PATH=$SCRIPT_PATH/$DIRNAME \
    CHANNELS_INCLUDE=$DIRNAME/manifest/reduce.channels.manifest.include \
    SEQUENTIAL_ID=$SEQUENTIAL_ID \
    ./template.sh $DIRNAME/manifest/manifest.template | \
    sed s@r_red"$COUNTER"-@/dev/in/@g > $DIRNAME/manifest/reduce"$COUNTER".manifest
#gennvram
    NODEID=$COUNTER \
    ./template.sh $DIRNAME/nvram/reduce.nvram.template > $DIRNAME/nvram/reduce"$COUNTER".nvram
    let SEQUENTIAL_ID=SEQUENTIAL_ID+1
    let COUNTER=COUNTER+1 
done


