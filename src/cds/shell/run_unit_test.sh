#!/usr/bin/env bash


CDS=${HOME}/coding/baidu/bce/cds
UNIT_TEST=${CDS}/output/test/

cd ${UNIT_TEST}

for program in  `ls ${UNIT_TEST} | grep test | egrep -v io_man`;
do
    echo "run test programe------->${program}"
    ${UNIT_TEST}/${program}
    if [ $? -ne 0 ]; then
        echo "test ${program} fails"
        break
    fi
done


