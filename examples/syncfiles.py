# Add package dirmonitor to PATHONPATH
import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(path)

import time
from dirmonitor import DirMonitor
import subprocess

local_dir = "/Users/harley/workspace/weshop"
remote_dir = "/var/www/weshop"
remote_user = "root"
remote_host = "yunserver"


def callback(path):
    relative_path = path[len(local_dir)+1:]
    remote_path = os.path.join(remote_dir, relative_path)
    print("Detected " + relative_path + " changed. \nsending ......")
    command = "ssh " + remote_user + "@" + remote_host + " 'mkdir -p " + "/".join(remote_path.split("/")[:-1]) + "'"
    subprocess.check_call(command, shell=True, executable="/bin/bash")
    command = "scp " + path + " " + remote_user + "@" + remote_host + ":" + remote_path
    subprocess.check_call(command, shell=True, executable="/bin/bash")
    command = "ssh " + remote_user + "@" + remote_host + " 'touch " + remote_dir + "/weshop/wsgi.py'"
    subprocess.check_call(command, shell=True, executable="/bin/bash")
    print("Succeed sending " + relative_path + " to " + remote_host + ":" + remote_path + "\n")


if __name__ == "__main__":
    monitor = DirMonitor(target=local_dir, callback=callback)
    monitor.start()
    while True:
        time.sleep(5)

