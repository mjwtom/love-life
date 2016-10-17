#!/usr/bin/env bash

FINGERPRINT_SET='finger-fslhome-4k finger-src-4k finger-vm-4k'
FINGERPRINT_HOME=/media/indexDisk/mjw
SSD_HOME=/home/mjw/SSD
PROGRAM_HOME=/home/mjw/workspace/batch-dedupe/Debug
PROGRAM_SET='batch-dedup-bf-10 batch-bf'


test_bloom_filter()
{
for fingerprint in $FINGERPRINT_SET
do
    for program in $PROGRAM_SET
    do
    $PROGRAM_HOME/$program $SSD_HOME/meta $FINGERPRINT_HOME/$fingerprint > $program-$fingerprint .txt
    done
done
}

test_bloom_filter