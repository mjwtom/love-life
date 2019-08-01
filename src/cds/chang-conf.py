#!/user/sbin/env python

import os
import sys


def parse_line(line):
    parts = line.split('=')
    if len(parts) != 2:
        return '', ''
    flag = parts[0][2:]
    value  = parts[-1]
    return flag, value


def new_conf_line(flag, value):
    return '--' + flag + '=' + value


def change_conf_file_flag(path, new_flag, new_value):
    found = False
    lines = []
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            flag, value = parse_line(line)
            if flag != new_flag:
                lines.append(line)
                continue
            line = new_conf_line(new_flag, new_value)
            lines.append(line)
            found = True

    if not found:
        lines.append(new_conf_line(new_flag, new_value))

    with open(path, 'w') as f:
        for line in lines:
            f.write(line + os.linesep)


def change_all_conf(flag, value):
    names = os.listdir('.')
    print('confgs num %d' % len(names))
    for name in names:
        print('process ' + name)
        if name == '.' or name == '..':
            print('%s is not real dir' % name)
            continue
        if not os.path.isdir(name):
            continue
        if 'online' not in name:
            print('%s is not online config' % name)
            continue
        files = os.listdir(name)
        for file in files:
            if file == '.' or file == '..':
                continue
            path = os.path.join(name, file)
            if os.path.isdir(path):
                continue
            print('process ' + path)
            change_conf_file_flag(path, flag, value)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('python change-conf.py flag value')
        exit(-1)
    change_all_conf(sys.argv[1], sys.argv[2])
