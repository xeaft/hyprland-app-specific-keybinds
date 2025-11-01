import conf_parser
import pyinotify
import sys
import os
import time
import signal
from glog import logger

scr_path = os.path.dirname(__file__)
last_upd_time = time.time_ns() / 1000000

def on_change(_ev):
    global last_upd_time
    time.sleep(0.05)
    ms_now = time.time_ns() / 1000000

    if ms_now - last_upd_time < 150:
        return

    last_upd_time = ms_now
    pidfile = os.path.join(scr_path, ".pid")
    if not os.path.isfile(pidfile):
        logger.error("inotify > .pid not present")
        return

    pid = ""
    with open(pidfile, "r") as f:
        pid = f.read().strip()
    
    os.kill(int(pid), signal.SIGHUP)

def register_watcher():
    conf_loc = os.path.dirname(conf_parser.get_conf_file_loc())

    if (not len(conf_loc)):
        logger.critical("Failed to get config location for watcher.") 
        sys.exit(1)   

    wm = pyinotify.WatchManager()
    wm.add_watch(conf_loc, pyinotify.IN_MODIFY, on_change)
    wm.add_watch(conf_loc, pyinotify.IN_CREATE, on_change)
    notifier = pyinotify.Notifier(wm)
    notifier.loop()
