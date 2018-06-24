import subprocess
import json
import sys
import time


def get_disk_io(machines):
    disk_stats = []
    for machine in machines:
        cmd = 'curl "http://api.mt.noah.baidu.com:8557' \
          '/monquery/getlastestitemdata?' \
          'namespaces=%s&' \
              'items=DISK_TOTAL_READ_KB,DISK_TOTAL_WRITE_KB,' \
              'DISK_MAX_PARTITION_IO_UTIL"' % machine
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        disk_stat = json.loads(out)
        disk_stats.append(disk_stat)
    return disk_stats


def get_machines(noah_path):
    cmd = 'get_hosts_by_path % s' % noah_path
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    lines = out.split('\n')
    machines = []
    for line in lines:
        if not line.strip():
            continue
        machines.append(line.strip())
    return machines


def get_disk_info(noah_path):
    machines = get_machines(noah_path)
    print(machines)
    while True:
        disk_stat = get_disk_io(machines)
        print(disk_stat)
        time.sleep(10)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('give the noah path')
        exit(-1)
    get_disk_info(sys.argv[1])