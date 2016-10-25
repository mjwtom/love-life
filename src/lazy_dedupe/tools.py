#!/usr/bin/env python


hit = 21576173
dup = 21543460


def bloom_false_positive_rate(hit, dup):
    false_positive_num = hit - dup
    rate = float(false_positive_num)/hit
    return rate


if __name__ == '__main__':
    # 使用科学记数法输出
    print("bloom filter false positive rate: %e" % bloom_false_positive_rate(hit, dup))
