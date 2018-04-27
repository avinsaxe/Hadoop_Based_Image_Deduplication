import time
from threading import Thread
import os
import platform
import re

class Hadoop_Message_Parser:
    def __init__(self,path="output/hadoop_output.txt"):
        self.hadoop_file_path=path
        self.interval=3
        self.prev_timestamp=-1
        self.file=None
        self.duplicate_hashes=[]

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

    def __duplicate_identified__(self,hash):
        self.duplicate_hashes.append(hash)

    def parse_hadoop_output_file(self):
        print "\n\tParsing Hadoop Output File"
        with open(self.hadoop_file_path) as fp:
            lines=fp.readlines()
            for line in lines:
                line=line.strip()
                line_split=self.split_multiple_spaces(line)
                print line_split
                if len(line_split)<2:
                    continue
                if int(line_split[1])>1:
                    self.__duplicate_identified__(line_split[0])

        print "Duplicate Hashes List ",self.duplicate_hashes




    def split_multiple_spaces(self, l=""):
            if l == "":
                return None
            splits = re.split(r'\s{1,}', l)
            splits = [i for i in splits if i != '']
            return splits


    def poll_continuously(self):
        while(True):
            print "Polling directory ",self.hadoop_file_path

            time.sleep(self.interval)
            last_updated_timestamp= self.__get_last_update_timestamp__(self.hadoop_file_path)
            if last_updated_timestamp>self.prev_timestamp:
                self.prev_timestamp=last_updated_timestamp
                self.parse_hadoop_output_file()