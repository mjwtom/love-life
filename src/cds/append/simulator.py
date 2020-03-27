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
    def __init__(self, distribution=True # is random
                       , s=4 * 1024  # write size
                       , o=1.0  # oversell rate
                       , P=3.5 * 1024 * 1024 * 1024 * 1024  # physical space
                       , M=16 * 1024 * 1024 * 1024  # segment size
                       , u=0.9  # compaction start point
                        , compaction_to_diff_seg=False # compaction write to diff seg
                        , check_after_compaction=True
                       ):
        self.P = P
        self.M = M
        self.s = s
        self.o = o
        self.u = u
        self.S = P * o
        self.distribution = distribution
        self.compaction_to_diff_seg = compaction_to_diff_seg
        self.check_after_compaction = check_after_compaction

        # previous write pos
        pos_num = self.S/self.s
        self.pre_write_seg = []
        for i in range(int(pos_num)):
            self.pre_write_seg.append((-1,-1)) # segment id

        # segments
        self.seg_blk_num = M / s
        self.segment_map = dict()
        self.segment_index = 1
        self.current_seg = Segment(self.segment_index, self.seg_blk_num)
        self.segment_map[self.segment_index] = self.current_seg
        self.seg_pos = 0
        self.write_seg_index = self.segment_index

        # compaction_seg
        self.segment_index += 1
        self.compaction_seg = Segment(self.segment_index, self.seg_blk_num)
        self.segment_map[self.segment_index] = self.compaction_seg
        self.compaction_seg_pos = 0
        self.compaction_seg_index = self.segment_index

        # metrics
        self.write_count = 0
        self.compaction_count = 0
        self.pre_write_count = 0
        self.pre_compaction_count = 0

    def get_write_pos(self):
        if self.distribution:
            return random.randint(0, int(self.S/self.s) - 1)

    def check(self):
        for seg in self.segment_map.values():
            for i in range(len(seg.data)):
                offset = seg.data[i]
                if offset == -1:
                    continue
                seg_index, pos = self.pre_write_seg[offset]
                if seg_index != seg.seg_id:
                    print('offset %d, seg not match, pre_write_index_seg: %d, check_seg_id: %d' %
                          (offset, seg_index, seg.seg_id))
                    exit(-1)
                if pos != i:
                    print('offset %d, seg pos not match' % offset)
                    exit(-1)
        for offset in range(len(self.pre_write_seg)):
            seg_index, seg_pos = self.pre_write_seg[offset]
            if seg_index == -1:
                continue
            seg = self.segment_map.get(seg_index)
            if not seg:
                print('can not get segment %d' % seg_index)
                exit(-1)
            record_offset = seg.data[seg_pos]
            if record_offset != offset:
                print('offset not match')
                exit(-1)

    def compaction(self):
        free = 0
        segment = None
        found_write_seg = False
        found_compaction_seg = False
        for seg in self.segment_map.values():
            if seg == self.current_seg:
                found_write_seg = True
                continue
            if seg == self.compaction_seg:
                found_compaction_seg = True
                continue
            cur_free = seg.free_num()
            if cur_free > free:
                segment = seg
                free = cur_free
        if segment:
            print("compaction %d" % segment.seg_id)
            for offset in segment.data:
                if offset == -1:
                    continue
                self.compaction_write(offset)
                self.compaction_count += 1
            free_num = segment.free_num()
            max_blk_num = segment.max_blk_num
            # print('free: %d, max: %d, len %d' % (free_num, max_blk_num, len(segment.data)))
            if free_num >= max_blk_num:
                delta_write_count = self.write_count - self.pre_write_count
                delta_compaction_count = self.compaction_count - self.pre_compaction_count
                self.segment_map.pop(segment.seg_id)
                print("free segment %d" % segment.seg_id)
                if delta_write_count > 0:
                    print('write_count %d, compaction_count: %d, %f' %
                        (delta_write_count, delta_compaction_count, delta_compaction_count*1.0/delta_write_count))
                    self.pre_write_count = self.write_count
                    self.pre_compaction_count = self.compaction_count
        if not self.check_after_compaction:
            return
        if not found_write_seg or not found_compaction_seg:
            print('not found write or compaction seg')
            exit(-1)
        self.check()

    def invalid_pre_write(self, offset):
        pre, pos = self.pre_write_seg[offset]
        if pre >= 0:
            segment = self.segment_map.get(pre)
            segment.invalid(pos)

    def write(self, offset):
        self.invalid_pre_write(offset)
        if self.seg_pos >= self.seg_blk_num:
            self.segment_index += 1
            print('new write seg: %d' % self.segment_index)
            self.current_seg = Segment(self.segment_index, self.seg_blk_num)
            self.segment_map[self.segment_index] = self.current_seg
            self.write_seg_index = self.segment_index
            self.seg_pos = 0
        self.current_seg.write(offset)
        self.pre_write_seg[offset] = (self.write_seg_index, self.seg_pos)
        self.seg_pos += 1

    def compaction_write(self, offset):
        if not self.compaction_to_diff_seg:
            self.write(offset)
            return
        self.invalid_pre_write(offset)
        if self.compaction_seg_pos >= self.seg_blk_num:
            self.segment_index += 1
            print('new compaction seg: %d' % self.segment_index)
            self.compaction_seg = Segment(self.segment_index, self.seg_blk_num)
            self.segment_map[self.segment_index] = self.compaction_seg
            self.compaction_seg_index = self.segment_index
            self.compaction_seg_pos = 0
        self.compaction_seg.write(offset)
        self.pre_write_seg[offset] = (self.compaction_seg_index, self.compaction_seg_pos)
        self.compaction_seg_pos += 1

    def process(self):
        # start to write
        self.write_count = 0
        while True:
            offset = self.get_write_pos()
            self.write(offset)
            self.write_count += 1
            while len(self.segment_map) * self.M > self.P * self.u:
                self.compaction()


def simulate():
    sim = AppendSim(distribution=True # writes distribution
                    , s=4 * 1024  # write size
                    , o=0.9  # oversell rate
                    , P=48 * 1024 * 1024 * 1024  # physical size
                    , M=16 * 1024 * 1024  # segment size
                    , u=0.8  # compaction start point
                    , compaction_to_diff_seg=True
                    , check_after_compaction=False
                       )
    sim.process()


if __name__ == '__main__':
    simulate()

