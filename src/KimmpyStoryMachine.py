import os
import sys
import random


def random_rename(path):
    if not os.path.exists(path):
        print('The given directory does not exist: %s' % path)
        return
    if not os.path.isdir(path):
        print('The path is not a directory %s' % path)
        return
    files = os.listdir(path)
    random.shuffle(files)
    i = 1
    for f in files:
        suffix = f[3:]
        prefix = '%03d' % i
        i += 1
        cur_name = prefix+suffix
        src = os.path.join(path, f)
        dst = os.path.join(path, cur_name)
        print('%s---->%s' % (src, dst))
        os.rename(src, dst)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('please give the directory name')
        exit(0)
    dir_name = sys.argv[1]
    random_rename(dir_name)
