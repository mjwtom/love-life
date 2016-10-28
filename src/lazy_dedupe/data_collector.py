#!/usr/bin/env python
import os


def get_bf_test():
    base_dir = 'E:\\lazy dedupe\\bf-test'
    eager_time = 0.0
    lazy_time = 0.0
    for bf in ['32', '64', '128', '256', '512', '1024']:
        for data in ['vm', 'src', 'fslhome']:
            print('\n')
            for method in ['eager', 'lazy']:
                sum_on_disk_lookup = 0.0
                on_disk_lookup_count = 0.0
                sum_prefetch = 0.0
                prefetch_count = 0
                sum_identification = 0.0
                identification_count = 0
                for i in range(10):
                    file_name = 'finger-'+data+'-4k-batch-dedupe-'+method+'-'+bf+('-%d'%i)+'.txt'
                    file_path = os.path.join(base_dir, file_name)
                    on_disk_lookup, prefetch, identification = get_data(file_path)
                    if on_disk_lookup != 0.0:
                        text = 'on disk lookup time: %f' % on_disk_lookup
                        # print(text)
                        sum_on_disk_lookup += on_disk_lookup
                        on_disk_lookup_count += 1
                    if prefetch != 0.0:
                        text = 'prefetch: %f' % prefetch
                        # print(text)
                        sum_prefetch += prefetch
                        prefetch_count += 1
                    if identification != 0.0:
                        text = 'identification: %f' % identification
                        # print(text)
                        sum_identification += identification
                        identification_count += 1
                print(bf, data, method, ':')
                text = 'average on disk lookup time: %f' % (sum_on_disk_lookup / on_disk_lookup_count)
                print(text)
                text = 'average prefetching time: %f' % (sum_prefetch / prefetch_count)
                print(text)
                text = 'average identification time: %f' % (sum_identification / identification_count)
                print(text)
                if method == 'eager':
                    eager_time = sum_identification/identification_count
                else:
                    lazy_time = sum_identification/identification_count
                    improvement(eager_time, lazy_time)


def get_data(file_path):
    on_disk_lookup = 0.0
    prefetch = 0.0
    identification = 0.0
    # if file not exist
    if not os.path.exists(file_path):
        return on_disk_lookup, prefetch, identification

    with open(file_path) as f:
        for line in f:
            if line.startswith('disk hash lookup time'):
                data = line.split()
                on_disk_lookup = float(data[-1])
            elif line.startswith('load cache read time'):
                data = line.split()
                prefetch = float(data[-1])
            elif line.startswith('identify time'):
                data = line.split()
                identification = float(data[-1])
    return on_disk_lookup, prefetch, identification


def get_fslhomes_data():
    fshmomes_base_dir = 'E:\\lazy dedupe\\batch-dedupe\\fslhomes-fslhomes'
    sum_on_disk_lookup = 0.0
    on_disk_lookup_count = 0
    sum_prefetch = 0.0
    prefetch_count = 0
    sum_identification = 0.0
    identification_count = 0
    for i in range(0, 10):
        file_path = os.path.join(fshmomes_base_dir, 'round-%d'%i, 'eager.txt_')
        on_disk_lookup, prefetch, identification = get_data(file_path)
        if on_disk_lookup != 0.0:
            text = 'on disk lookup time: %f' % on_disk_lookup
            print(text)
            sum_on_disk_lookup += on_disk_lookup
            on_disk_lookup_count += 1
        if prefetch != 0.0:
            text = 'prefetch: %f' % prefetch
            print(text)
            sum_prefetch += prefetch
            prefetch_count += 1
        if identification != 0.0:
            text = 'identification: %f' % identification
            print(text)
            sum_identification += identification
            identification_count += 1
    average_on_disk_lookup = sum_on_disk_lookup/on_disk_lookup_count
    text = 'average on disk lookup time: %f' % (sum_on_disk_lookup/on_disk_lookup_count)
    print(text)
    average_prefetch = sum_prefetch/prefetch_count
    text = 'average prefetching time: %f' % (sum_prefetch/prefetch_count)
    print(text)
    average_identification = sum_identification/identification_count
    text = 'average identification time: %f' % (sum_identification/identification_count)
    print(text)
    return average_on_disk_lookup, average_prefetch, average_identification


def get_vm_data():
    fshmomes_base_dir = 'E:\\lazy dedupe\\batch-dedupe'
    sum_on_disk_lookup = 0.0
    on_disk_lookup_count = 0
    sum_prefetch = 0.0
    prefetch_count = 0
    sum_identification = 0.0
    identification_count = 0
    for i in range(1, 11):
        file_path = os.path.join(fshmomes_base_dir, 'round-%d'%i, 'eager-vm.txt_')
        on_disk_lookup, prefetch, identification = get_data(file_path)
        if on_disk_lookup != 0.0:
            text = 'on disk lookup time: %f' % on_disk_lookup
            print(text)
            sum_on_disk_lookup += on_disk_lookup
            on_disk_lookup_count += 1
        if prefetch != 0.0:
            text = 'prefetch: %f' % prefetch
            print(text)
            sum_prefetch += prefetch
            prefetch_count += 1
        if identification != 0.0:
            text = 'identification: %f' % identification
            print(text)
            sum_identification += identification
            identification_count += 1
    average_on_disk_lookup = sum_on_disk_lookup/on_disk_lookup_count
    text = 'average on disk lookup time: %f' % (sum_on_disk_lookup/on_disk_lookup_count)
    print(text)
    average_prefetch = sum_prefetch/prefetch_count
    text = 'average prefetching time: %f' % (sum_prefetch/prefetch_count)
    print(text)
    average_identification = sum_identification/identification_count
    text = 'average identification time: %f' % (sum_identification/identification_count)
    print(text)
    return average_on_disk_lookup, average_prefetch, average_identification


def get_src_data():
    fshmomes_base_dir = 'E:\\lazy dedupe\\batch-dedupe'
    sum_on_disk_lookup = 0.0
    on_disk_lookup_count = 0
    sum_prefetch = 0.0
    prefetch_count = 0
    sum_identification = 0.0
    identification_count = 0
    for i in range(1, 11):
        file_path = os.path.join(fshmomes_base_dir, 'round-%d'%i, 'eager-src.txt_')
        on_disk_lookup, prefetch, identification = get_data(file_path)
        if on_disk_lookup != 0.0:
            text = 'on disk lookup time: %f' % on_disk_lookup
            print(text)
            sum_on_disk_lookup += on_disk_lookup
            on_disk_lookup_count += 1
        if prefetch != 0.0:
            text = 'prefetch: %f' % prefetch
            print(text)
            sum_prefetch += prefetch
            prefetch_count += 1
        if identification != 0.0:
            text = 'identification: %f' % identification
            print(text)
            sum_identification += identification
            identification_count += 1
    average_on_disk_lookup = sum_on_disk_lookup/on_disk_lookup_count
    text = 'average on disk lookup time: %f' % (sum_on_disk_lookup/on_disk_lookup_count)
    print(text)
    average_prefetch = sum_prefetch/prefetch_count
    text = 'average prefetching time: %f' % (sum_prefetch/prefetch_count)
    print(text)
    average_identification = sum_identification/identification_count
    text = 'average identification time: %f' % (sum_identification/identification_count)
    print(text)
    return average_on_disk_lookup, average_prefetch, average_identification


base_time = 5824
opt_time = 3939


def improvement(base_time, opt_time):
    base_throughput = 1.0/base_time
    opt_throughput = 1.0/opt_time
    improve = (opt_throughput-base_throughput)/base_throughput
    if improve < 1:
        text = '%f%%' % (improve*100)
    else:
        text = 'x%f' % improve
    print(text)


if __name__ == '__main__':
    # improvement(base_time, opt_time)
    # get_src_data()
    get_bf_test()
