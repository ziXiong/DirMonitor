DirMonitor
==========
Set to monitor a directory, call a callback whenever file changed under this directory

Examples
========


    from dirmonitor import DirMonitor

    def callback(filepath):
        print(filepath + "has changed!")

    monitor = DirMonitor(target="/var/www", callback=callback)
    monitor.start()
