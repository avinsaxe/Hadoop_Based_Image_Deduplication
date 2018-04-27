import time
from threading import Thread
import os
import platform
from Image_Processing import *
from dupSearch import *
import re


#needs to be one object in main file, with reset of duplicate_hashes everytime the data is displayed

class Hadoop_Message_Parser:
    def __init__(self,path="output/hadoop_output.txt"):
        self.hadoop_file_path=path
        self.interval=3
        self.prev_timestamp=-1
        self.file=None
        self.duplicate_hashes=[]
        self.image_processing=ImageProcessing()
        self.repeat_images=[]


    #href:: StackOverflow
    def __get_last_update_timestamp__(self,path):
        if platform.system() == 'Windows':
            return os.path.getctime(path)
        else:
            stat = os.stat(path)
            try:
                return stat.st_birthtime
            except AttributeError:
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
        self.finder = Finder()
        print "Duplicate Hashes List ",self.duplicate_hashes
        if self.duplicate_hashes!=None and len(self.duplicate_hashes)>0:
            print "Duplicate Printing"
            for i in range(0,len(self.duplicate_hashes)):
                temp=self.finder.get_image_path_from_hash(self.duplicate_hashes[i])
                self.repeat_images=self.repeat_images+temp


            self.duplicate_hashes=[]  #reset the duplicate hashes
        self.__thread_display_output_console__()
        self.repeat_images=[]



    def split_multiple_spaces(self, l=""):
            if l == "":
                return None
            splits = re.split(r'\s{1,}', l)
            splits = [i for i in splits if i != '']
            return splits

    def __thread_display_output_console__(self):
        print "Repeating "
        if self.repeat_images!=None and len(self.repeat_images)>0:
            print "Repeating Images "
            for image in self.repeat_images:
                print image["_id"]


    def poll_continuously(self):
        while(True):
            print "Polling directory ",self.hadoop_file_path

            time.sleep(self.interval)
            last_updated_timestamp= self.__get_last_update_timestamp__(self.hadoop_file_path)
            if last_updated_timestamp>self.prev_timestamp:
                self.prev_timestamp=last_updated_timestamp
                self.parse_hadoop_output_file()