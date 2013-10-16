#!/bin/bash
ZEROVM="${ZVM_PREFIX}/bin/zerovm -QPs"
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

ZVM_REPORT=report.txt
rm data/*sorted* log/* -f ${ZVM_REPORT}

./ns_start.sh 2
sed "s@{ABS_PATH}@$SCRIPTPATH/@" manifest/map.manifest.template > manifest/map.manifest
sed "s@{ABS_PATH}@$SCRIPTPATH/@" manifest/reduce.manifest.template > manifest/reduce.manifest

${SETARCH} ${ZEROVM} manifest/map.manifest >> ${ZVM_REPORT} &
${SETARCH} ${ZEROVM} manifest/reduce.manifest >> ${ZVM_REPORT} &

for job in `jobs -p`
do
    wait $job
done

./ns_stop.sh

~/git/zerovm-llvm/terasort/valsort data/1sorted.dat
