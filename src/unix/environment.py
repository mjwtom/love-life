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
        self.bin = 'bin'

    def install_dependency(self):
        software_list = ['libncurses5-dev']
        cmd = 'sudo apt-install '+' '.join(software_list)
        subprocess.call(cmd, shell=True)

    def mkdirs(self):
        # The directory to install softwares
        path = os.path.join(self.home_dir, self.install_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        # The directory for downloading
        path = os.path.join(self.home_dir, self.download_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        path = os.path.join(self.home_dir, self.bin)
        if not os.path.exists(path):
            os.mkdir(path)

    def configure_bash_profiling(self):
        path = os.path.join(self.home_dir, '.bash_profile')
        with open(path, 'w') as bash_profiling:
            bin_path = os.path.join(self.home_dir, self.bin)
            cmd = 'export PATH='+bin_path+':$PATH'+'\n'
            bash_profiling.write(cmd)
            install_path = os.path.join(self.home_dir, self.install_dir)
            cmd = 'export JAVA_HOME='+install_path+'/jdk1.8.0_111'+'\n'
            bash_profiling.write(cmd)

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
        path = os.path.join(self.home_dir, self.bin)
        os.chdir(path)
        cmd = 'ln -s '+os.path.join(install_path, 'bin', 'vim')
        subprocess.call(cmd, shell=True)

    def configure_vim(self):
        path = os.path.join(self.home_dir, self.download_dir)
        os.chdir(path)
        subprocess.call('curl https://j.mp/spf13-vim3 -L > spf13-vim.sh && sh spf13-vim.sh', shell=True)


def process():
    env = Environment()
    env.mkdirs()
    env.install_vim()
    env.configure_vim()
    env.configure_bash_profiling()


if __name__ == '__main__':
    process()
