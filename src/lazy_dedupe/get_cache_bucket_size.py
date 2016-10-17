#!/usr/bin/env python
import sys

# define some constants
total_memory = 256 * 1024 * 1024
cache_item_size = 48
buffer_item_size = 4096
buffer_index_len = 1024
cache_index_len = 128 * 1024


def get_cache_bucket_size(threshold):
    buffer_memory = threshold * buffer_index_len * buffer_item_size
    print('buffer memory size: %f MB' % (buffer_memory / 1024 / 1024))
    cache_memory = total_memory - buffer_memory
    print('cache memory size: %f MB' % (float(cache_memory) / 1024 / 1024))
    return float(cache_memory) / cache_index_len / cache_item_size


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('please give the fingerprint buffer threshold')
    else:
        print('cache bucket size: %f' % get_cache_bucket_size(int(sys.argv[1])))
