#!/usr/bin/env python
import os
import subprocess


FINGERPRINT_SET=['finger-src-4k', 'finger-vm-4k', 'finger-fslhome-4k']
#FINGERPRINT_SET=['fake-finger-fslhome-4k', 'fake-finger-src-4k', 'fake-finger-vm-4k']
FINGERPRINT_HOME='/media/indexDisk/mjw'
SSD_HOME='/home/mjw/SSD'
PROGRAM_HOME='/home/mjw/workspace/batch-dedupe/Debug'

PROGRAM_SET=['batch-dedupe-eager-1024',  'batch-dedupe-eager-512',  'batch-dedupe-lazy-256',
            'batch-dedupe-eager-128',   'batch-dedupe-eager-64',   'batch-dedupe-lazy-32',
            'batch-dedupe-eager-256',   'batch-dedupe-lazy-1024',  'batch-dedupe-lazy-512',
            'batch-dedupe-eager-32',    'batch-dedupe-lazy-128',   'batch-dedupe-lazy-64']


def test_bloom_filter():
    for i in range(10):
        for program in PROGRAM_SET:
            for fingerprint in FINGERPRINT_SET:
                program_path = os.path.join(PROGRAM_HOME, program)
                metadata_path = os.path.join(SSD_HOME, 'meta')
                fingerprint_path = os.path.join(FINGERPRINT_HOME, fingerprint)
                result_name = fingerprint+'-'+program+'-'+str(i)+'.txt'
                cmd = [program_path,
                    metadata_path,
                    fingerprint_path,
                    '>',
                    result_name]
                cmd = ' '.join(cmd)
                print(cmd)
                subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    test_bloom_filter()
