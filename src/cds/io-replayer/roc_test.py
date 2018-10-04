import sys
import os
import uuid
import subprocess
from replay import replay

cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(cwd)
sys.path.append(cwd)
from utils.cmd import Command
from utils.cmd import read_config


def create_root_volume(commander, image_id):
    volume_uuid = uuid.uuid4()
    job_uuid = uuid.uuid4()
    cmd = 'clone_volume --bootable=true' \
          ' --volume_uuid=%s --job_uuid=%s' \
          ' --snapshot_uuid=%s --disk_type=ssd' % (volume_uuid, job_uuid, image_id)
    commander.cds_cmd_and_check(cmd)
    commander.wait_job(job_uuid)
    return volume_uuid


def delete_root_volume(commander, volume_uuid):
    job_uuid = uuid.uuid4()
    cmd = 'delete_volume --need_snapshot=false' \
          ' --volume_uuid=%s --job_uuid=%s' \
          % (volume_uuid, job_uuid)
    commander.cds_cmd_and_check(cmd)
    commander.wait_job(job_uuid)
    return volume_uuid


def attach_volume(iscsi_shell_dir, commander, volume_uuid):
    cmd = 'stat_volume --volume_uuid=%s' % (volume_uuid)
    out = commander.cds_cmd(cmd)
    evm_id = out.get('volume_info').get('evm_id')
    cwd = os.getcwd()
    os.chdir(iscsi_shell_dir)
    shell_cmd = './iscsi.func.sh' \
                ' attach %d %s' % (evm_id, volume_uuid)
    print(shell_cmd)
    p = subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    os.chdir(cwd)
    if out:
        return out.strip()
    if err:
        print(err)
    else:
        return None


def detach_volume(iscsi_shell_dir, commander, volume_uuid):
    cmd = 'stat_volume --volume_uuid=%s' % (volume_uuid)
    out = commander.cds_cmd(cmd)
    evm_id = out.get('volume_info').get('evm_id')
    cwd = os.getcwd()
    os.chdir(iscsi_shell_dir)
    shell_cmd = './iscsi.func.sh' \
                ' detach %d %s' % (evm_id, volume_uuid)
    print(shell_cmd)
    p = subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    os.chdir(cwd)
    if out:
        return out.strip()
    if err:
        print(err)
    else:
        return None


def test():
    conf = read_config('cds.conf')
    cds_tool = conf.get('CDS', 'cds_tool')
    cds_master = conf.get('CDS', 'master')
    cds_token = conf.get('CDS', 'token')
    image_uuid = conf.get('CDS', 'image_uuid')
    iscsi_shell_dir = conf.get('iSCSI', 'shell_dir')
    cmd = Command(cds_tool, cds_master, cds_token, logger=None)
    volume_uuid = create_root_volume(cmd, image_uuid)
    dev = attach_volume(iscsi_shell_dir, cmd, volume_uuid)
    print(dev)
    replay(dev, 'io.json')
    detach_volume(iscsi_shell_dir, cmd, volume_uuid)
    delete_root_volume(cmd, volume_uuid)


if __name__ == '__main__':
    test()
