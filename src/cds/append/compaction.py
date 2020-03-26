#!/usr/bin/env python
import math


def valid_rate(m = 0 # segment第一次写位置
    , s = 4 * 1024 # 用户写大小
    , o = 1.0 # 超售比
    , P = 3.5 * 1024 * 1024 * 1024 * 1024 # 物理空间大小
    , M = 16 * 1024 * 1024 * 1024 # segment 大小
    , u = 0.9 # 物理空间使用率
    ):
    S = P * o
    n = P * u / s
    p = 1 - s * 1.0 / S # 每次写一个位置不被覆盖的概率
    valid_data = s * (math.pow(p, n-m-M/s) - math.pow(p, n-m+1)) / (1-p)
    return (valid_data/M)
    # print('有效数据率: %f' % pow(p, n))
