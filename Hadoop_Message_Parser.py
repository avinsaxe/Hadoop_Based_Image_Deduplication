import time
from threading import Thread
import os
import platform

class Hadoop_Message_Parser:
    def __init__(self,path="output/hadoop_output.txt"):
        self.hadoop_file_path=path
        self.interval=3
        self.prev_timestamp=-1

    def __get_last_update_timestamp__(self,path):
        if platform.system() == 'Windows':
            return os.path.getctime(path)
        else:
            stat = os.stat(path)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return stat.st_mtime

    def poll_continuously(self):
        while(True):
            print "Polling directory ",self.hadoop_file_path

            time.sleep(self.interval)
            print self.__get_last_update_timestamp__(self.hadoop_file_path)