import fnmatch
import os
import sys
import threading
import atexit
from queue import Queue
import time
import re
import subprocess


class Monitor():
    def __init__(self, callback=None, local_dir=None, remote_dir=None, remote_user=None, remote_host=None):
        self.local_dir, self.remote_dir, self.remote_user, self.remote_host = local_dir, remote_dir, remote_user, remote_host
        if not local_dir:
            raise Exception("local path cannot be None!")
        if self.local_dir[-1] == "/":
            self.local_dir = local_dir[:-1]
        if self.remote_dir and self.remote_dir[-1] == "/":
            self.remote_dir = remote_dir[:-1]
        self._interval = 1.0
        self._times = {}
        self._files = []
        self._running = False
        self._lock = threading.Lock()
        self.ignore_path = os.path.join(self.local_dir, ".gitignore")
        self.callback = callback or self._callback
        self._thread = threading.Thread(target=self._monitor)
        self._thread.setDaemon(True)
        atexit.register(self._exiting)

    def _monitor(self):
        self._update_ignore()
        while True:
            queue = Queue()
            queue.put(self.local_dir)
            # Check modification times on all files under local_dir.
            while not queue.empty():
                dir_path = queue.get()
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    if not self._ignored(item_path):
                        if os.path.isdir(item_path):
                            queue.put(item_path)
                        elif self._modified(item_path):
                            if item == ".gitignore":
                                self._update_ignore()
                            self.callback(item_path)
            time.sleep(1)

    def _ignored(self, item_path):
        if os.path.isdir(item_path):
            item_path += "/"
        for pattern in self.ignore_pattern:
            regex = fnmatch.translate(pattern)
            if re.search(regex, item_path[len(self.local_dir):]):
                return True
        return False

    def _update_ignore(self):
        self.ignore_pattern = []
        if os.path.isfile(self.ignore_path):
            with open(self.ignore_path, "r+") as file:
                pattern = re.compile(r"\s*#")
                lines = file.readlines()
                for line in lines:
                    if not pattern.match(line):
                        self.ignore_pattern.append(line[:-1])
        self.ignore_pattern.append(".git/")


    def start(self, interval=1.0):
        if interval < self._interval:
            self._interval = interval

        self._lock.acquire()
        if not self._running:
            prefix = 'monitor (pid=%d):' % os.getpid()
            print('%s Starting change monitor.' % prefix, file=sys.stderr)
            self._running = True
            self._thread.start()
        self._lock.release()

    def _exiting(self):
        self._thread.join()

    def _modified(self, path):
        try:
            if not os.path.isfile(path):
                return False

            # Check for when file last modified.
            mtime = os.stat(path).st_mtime
            if path not in self._times:
                self._times[path] = mtime
                return False
            elif mtime != self._times[path]:
                self._times[path] = mtime
                return True

        except:
            return True

        return False

    def track(self, path):
        if not path in self._files:
            self._files.append(path)

    def _callback(self, path):
        relative_path = path[len(self.local_dir)+1:]
        remote_path = os.path.join(self.remote_dir, relative_path)
        print("Detected " + relative_path + " changed. \nsending ......")
        command = "ssh " + self.remote_user + "@" + self.remote_host + " 'mkdir -p " + "/".join(remote_path.split("/")[:-1]) + "'"
        subprocess.check_call(command, shell=True, executable="/bin/bash")
        command = "scp " + path + " " + self.remote_user + "@" + self.remote_host + ":" + remote_path
        subprocess.check_call(command, shell=True, executable="/bin/bash")
        print("Succeed sending " + relative_path + " to " + self.remote_host + ":" + remote_path + "\n")


if __name__ == "__main__":
    monitor = Monitor(local_dir="/Users/harley/workspace/Django-autodeploy", remote_dir="/www/Django-autodeploy",
                      remote_user="root", remote_host="yunserver")
    monitor.start()
    while True:
        time.sleep(5)









