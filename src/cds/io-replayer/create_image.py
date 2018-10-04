import sys
import os
import uuid
import subprocess
from roc_test import attach_volume, detach_volume
import mmap


cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(cwd)
sys.path.append(cwd)
from utils.cmd import Command
from utils.cmd import read_config


BLOCK_SIZE_BYTES = 64 * 1024 * 1024


def get_disk_size(blockdev):
    blocks = int(open('/sys/block/{blockdev}/size'.format(**locals())).read())
    return blocks * 512


def fill_random_data(dev):
    size = get_disk_size(dev)
    info = 'volume size in %d GB' % (size / 1024 / 1024 /1024)
    print(info)
    with open("/dev/urandom", "rb") as f:
        buf = f.read(BLOCK_SIZE_BYTES)
    num = size / BLOCK_SIZE_BYTES
    path = os.path.join('/dev', dev)
    if not os.path.exists(path):
        print('device not exist')
        return
    f = os.open(path, os.O_DIRECT | os.O_RDWR)
    for i in range(int(num)):
        info = 'round %d left %d' % (i, num - i)
        print(info)
        m = mmap.mmap(-1, BLOCK_SIZE_BYTES)
        m.write(buf)
        os.write(f, m)
    os.close(f)


def create_root_volume(commander, size_gb):
    volume_uuid = uuid.uuid4()
    cmd = 'create_volume --bootable=true' \
          ' --volume_uuid=%s --volume_size=%s' \
          ' --disk_type=ssd' % (volume_uuid, size_gb)
    commander.cds_cmd_and_check(cmd)
    return volume_uuid


def convert_image(commander, volume_uuid, image_uuid):
    job_uuid = uuid.uuid4()
    cmd = 'create_snapshot --convert_image=true' \
          ' --volume_uuid=%s --snapshot_uuid=%s' \
          ' --job_uuid=%s' % (volume_uuid, image_uuid, job_uuid)
    commander.cds_cmd_and_check(cmd)
    commander.wait_job(job_uuid)
    return volume_uuid


def create_image_according_to_conf():
    conf = read_config('cds.conf')
    cds_tool = conf.get('CDS', 'cds_tool')
    cds_master = conf.get('CDS', 'master')
    cds_token = conf.get('CDS', 'token')
    image_uuid = conf.get('CDS', 'image_uuid')
    iscsi_shell_dir = conf.get('iSCSI', 'shell_dir')
    cmd = Command(cds_tool, cds_master, cds_token, logger=None)
    volume_uuid = create_root_volume(cmd, 40)
    dev = attach_volume(iscsi_shell_dir, cmd, volume_uuid)
    dev = os.path.split(dev)[-1]
    fill_random_data(dev)
    detach_volume(iscsi_shell_dir, cmd, volume_uuid)
    convert_image(cmd, volume_uuid, image_uuid)


if __name__ == '__main__':
    create_image_according_to_conf()
