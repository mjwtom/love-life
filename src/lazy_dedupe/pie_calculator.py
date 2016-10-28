#!/usr/bin/env python


chunk_speed = 217
#chunk_speed = 899
###########################################
hash_speed = 338
#hash_speed = 1563
###########################################
#data_size = 220.85*1024
#data_size = 434.88*1024
data_size = 3580*1024
###########################################
identification_time = 5824 # eager FSLHomes
#identification_time = 3939 # lazy FSLHomes



def get_chunk_hash_disk():
    chunk_time = data_size/chunk_speed
    hash_time = data_size/hash_speed
    print('chunk time: %f' % chunk_time)
    print('hash time: %f' % hash_time)
    print('identification time: %f' % identification_time)

    sum_time = chunk_time + hash_time + identification_time
    chunk_fraction = float(chunk_time)/sum_time
    hash_fraction = float(hash_time)/sum_time
    identification_fraction = float(identification_time)/sum_time
    print('chunk fraction: %f' % chunk_fraction)
    print('hash fraction: %f' % hash_fraction)
    print('identification fraction: %f' % identification_fraction)


if __name__ == '__main__':
    get_chunk_hash_disk()
