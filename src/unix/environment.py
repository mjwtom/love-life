#!usr/bin/env python

'''
This is the script used by majingwei to create his working environment on *nix Systems,
including Linux, Mac
'''
import subprocess
import os


class Environment(object):
    def __init__(self):
        self.home_dir = '/home/mjwtom'
        self.user='mjwtom'
        self.install_dir='install'
        self.download_dir = 'downloads'

    def mkdirs(self):
        # The directory to install softwares
        path = os.path.join(self.home_dir, self.install_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        # The directory for downloading
        path = os.path.join(self.home_dir, self.download_dir)
        if not os.path.exists(path):
            os.mkdir(path)

    def install_vim(self):
        path = os.path.join(self.home_dir, self.download_dir)
        os.chdir(path)
        subprocess.call('git clone https://github.com/vim/vim.git', shell=True)
        path = os.path.join(path, 'vim')
        os.chdir(path)
        install_path = os.path.join(self.home_dir, self.install_dir, 'vim')
        cmd = './configure --prefix='+install_path
        subprocess.call(cmd, shell=True)
        subprocess.call('make install', shell=True)


    def configure_vim(self):
        path = os.path.join(self.home_dir, self.download_dir)
        os.chdir(path)
        subprocess.call('curl https://j.mp/spf13-vim3 -L > spf13-vim.sh && sh spf13-vim.sh', shell=True)

def process():
    env = Environment()
    env.mkdirs()
    env.install_vim()
    env.configure_vim()



if __name__ == '__main__':
    process()