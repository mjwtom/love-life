#!/usr/bin/env python


#chunk_speed = 217
chunk_speed = 899
###########################################
#hash_speed = 338
hash_speed = 1563
###########################################
#data_size = 220.85*1024
#data_size = 434.88*1024
data_size = 3580*1024
###########################################
#identification_time = 151 # lazy vm
identification_time = 3939 # lazy vm



def get_chunk_hash_disk():
    chunk_time = data_size/chunk_speed
    hash_time = data_size/hash_speed
    print('chunk time: %f' % chunk_time)
    print('hash time: %f' % hash_time)
    print('identification time: %f' % identification_time)


if __name__ == '__main__':
    get_chunk_hash_disk()
