#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""

from os import path
from fabric.api import *
from datetime import datetime


env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'
env.hosts = ['100.25.153.251', '35.175.126.70']


def do_deploy(archive_path):
        """distributes an archive to your web servers
        """
        try:
                if not (path.exists(archive_path)):
                        return False

                put(archive_path, '/tmp/')
                timestamp = archive_path[-18:-4]
                run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(timestamp))

                run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
                    .format(timestamp, timestamp))

                run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))
                run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))
                run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'
                    .format(timestamp))

                run('sudo rm -rf /data/web_static/current')
                run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(timestamp))
        except:
                return False

        return True
