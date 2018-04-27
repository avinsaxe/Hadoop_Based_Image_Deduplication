import time
from threading import Thread
class Hadoop_Message_Parser:
    def __init__(self,path="output/hadoop_output.txt"):
        self.hadoop_file_path=path
        self.interval=3

    def poll_continuously(self):
        while(True):
            print "Polling directory ",self.hadoop_file_path
            time.sleep(self.interval)
