#!/usr/bin/env python
import random


class Segment(object):
    def __init__(self, seg_id, max_blk_num):
        self.count = 0
        self.seg_id = seg_id
        self.max_blk_num = max_blk_num
        self.data = []

    def invalid(self, pos):
        self.data[pos] = -1

    def write(self, offset):
        self.data.append(offset)

    def free_num(self):
        num = 0
        for val in self.data:
            if val == -1:
                num += 1
        return num


class AppendSim(object):
    def __init__(self, weight_gap=0 # 热点数据的前后gap
                       , s=4 * 1024  # 用户写大小
                       , o=1.0  # 超售比
                       , P=3.5 * 1024 * 1024 * 1024 * 1024  # 物理空间大小
                       , M=16 * 1024 * 1024 * 1024  # segment 大小
                       , u=0.9  # 物理空间使用率
                       ):
        self.P = P
        self.M = M
        self.weight_agp = weight_gap
        self.s = s
        self.o = o
        self.u = u
        # 主要目的是生成写的位置和表
        # 构建权重列表
        S = int(P * o)
        peak_pos = S/s/2
        weight_list = []
        weight = 1
        for i in range(int(peak_pos)):
            weight += weight_gap
            weight_list.append(weight)
        for i in range(int(peak_pos)):
            weight -= weight_gap
            weight_list.append(weight)
        # 通过权重列表，构建写的权重和位对应关系
        self.write_list = []
        for i in range(len(weight_list)):
            weight = weight_list[i]
            for j in range(weight):
                self.write_list.append(i)

        # 指向上一次写的位置，用来标记segment内的脏数据
        pos_num = S/s
        self.pre_write_seg = []
        for i in range(int(pos_num)):
            self.pre_write_seg.append((-1,-1)) # segment id

        # 还没有写产生，segment是空
        self.seg_blk_num = M / s
        self.segment_map = dict()
        self.segment_index = 1
        self.current_seg = Segment(self.segment_index, self.seg_blk_num)
        self.segment_map[self.segment_index] = self.current_seg
        self.seg_pos = 0

    def get_write_pos(self):
        index = random.randint(0, len(self.write_list)-1)
        return self.write_list[index]

    def compaction(self):
        free = 0
        segment = None
        for seg in self.segment_map.values():
            cur_free = seg.free_num()
            if cur_free > free:
                segment = seg
                free = cur_free
        if segment:
            print("compaction %d" % segment.seg_id)
            for offset in segment.data:
                if offset == -1:
                    continue
                self.write(offset)
            free_num = segment.free_num()
            max_blk_num = segment.max_blk_num
            # print('free: %d, max: %d, len %d' % (free_num, max_blk_num, len(segment.data)))
            if free_num >= max_blk_num:
                self.segment_map.pop(segment.seg_id)
                print("free segment %d" % segment.seg_id)

    def write(self, offset):
        pre, pos = self.pre_write_seg[offset]
        if pre >= 0:
            segment = self.segment_map.get(pre)
            segment.invalid(pos)
        if self.seg_pos >= self.seg_blk_num:
            self.segment_index += 1
            self.current_seg = Segment(self.segment_index, self.seg_blk_num)
            self.segment_map[self.segment_index] = self.current_seg
            self.seg_pos = 0
        self.current_seg.write(offset)
        self.pre_write_seg[offset] = (self.segment_index, self.seg_pos)
        self.seg_pos += 1

    def process(self):
        # 开始写
        write_count = 0
        while True:
            offset = self.get_write_pos()
            self.write(offset)
            write_count += 1
            while len(self.segment_map) * self.M > self.P * self.u:
                self.compaction()


def simulate():
    sim = AppendSim(weight_gap=0 # 热点数据的前后gap
                    , s=4 * 1024 * 1024  # 用户写大小
                    , o=0.5  # 超售比
                    , P=48 * 1024 * 1024  # 物理空间大小
                    , M=16 * 1024 * 1024  # segment 大小
                    , u=0.9  # 物理空间使用率
                       )
    sim.process()


if __name__ == '__main__':
    simulate()

