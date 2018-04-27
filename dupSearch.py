"""
"""
import os
import time
from flask_cors import CORS
import imagehash
from jinja2 import FileSystemLoader, Environment
from more_itertools import chunked
from PIL import Image, ExifTags
import pymongo
import DBConnection
import Constants
import imagehash
import magic
from pprint import pprint
from Image_Processing import ImageProcessing
from OutputCreator import *
from bson import json_util

from threading import Thread
from time import sleep
from hadoopMessageParser import *
import threading


class Finder:
    def __init__(self):
        self.db_path=""
        self.images=None
        self.img_processing=ImageProcessing()
        self.output=OuputCreator()

    def setup_db(self,db_path):
        self.db_path=db_path
        if db_path=="":
            self.images= DBConnection.connect()
        else:
            self.images= DBConnection.connect_db(db_path)

        pprint (self.images)

    def get_image_path_from_hash(self,hash=""):
        if self.images==None:
            self.setup_db(self.db_path)
        if hash=="" or self.images==None:
            return None
        all_images=self.images.find()
        all_images_with_required_hash=[]
        for image in all_images:
            if image["hash"]==hash:
                all_images_with_required_hash.append(image)

        return all_images_with_required_hash




    def add_hashes_to_file(self):
        if self.images==None:
            return
        all_images=self.images.find()
        hashes=[]
        print all_images[0]
        for i in range(0,all_images.count()):
            hashes.append(all_images[i]["hash"])
        self.output.write_hashes(hashes)

    def add_profiles_to_file(self):
        return
        # if self.images == None:
        #     return
        # all_images = self.images.find()
        # li=list(all_images)
        # data={}
        # data['root']=[]
        # print li
        # for i in range(0,len(li)):
        #     print li[i]
        #     data["root"].append(li[i])
        #
        # #json_data=json.dumps(li, default=json_util.default)
        # self.output.write_json(data)

    def execute(self,command=""):
        if command=="":
            return
        command_list=command.split(" ")
        if len(command_list)>1 and command_list[0]== Constants.command_start:
            #duplicate_search -add hashes_to_output

            if len(command_list)==3 and command_list[1]=="-db":
                db_path=command_list[2]
                if db_path=="default":
                    self.setup_db("")
                else:
                    self.setup_db(db_path)
            elif len(command_list)==3:
                if command_list[1]=="-add" and command_list[2]=="hashes_to_output":
                    self.add_hashes_to_file()

                    # duplicate_search -add profiles_to_output
                elif command_list[1] == "-add" and command_list[2] == "profiles_to_output":
                    self.add_profiles_to_file()
                elif command_list[1] == "-find":
                    if command_list[2] == "duplicates":
                        self.find_duplicates()

                elif command_list[1]=="-add":
                    folder_path=command_list[2]
                    if folder_path=="":
                        print "Empty folder"
                        return
                    else:
                        self.add_folder_path(folder_path)
                elif command_list[1]=="-remove":
                    folder_path=command_list[2]
                    if folder_path=="":
                        print "Empty folder"
                        return
                    else:
                        self.remove_images_from_path(folder_path)
            elif len(command_list)==2 and command_list[1]=="-show":
                self.show()
            elif len(command_list)==4 and command_list[1]=="-delete":
                delete_key=command_list[2]
                delete_value=command_list[3]
                self.delete(delete_key,delete_value)
            elif len(command_list)==3 and command_list[1]=="-db" and command_list[2]=="reset":
                self.reset_database()


    def find_duplicates(self):
        print "Identifying duplicates"
        all_images=self.images.find()  #gives a list of maps in json format
        for i in range(0,all_images.count()-1):
            for j in range(i+1,all_images.count()):
                #print all_images[i]["_id"], "  and  ", all_images[j]["_id"]
                isSimilar=self.img_processing.are_images_similar(all_images[i]["hash"],all_images[j]["hash"])
                if isSimilar==True:
                    print all_images[i]," and ",all_images[j]," are similar "



    def add_image_to_database_with_hash(self,file, hashes, size_on_disk, size, timestamp):
        if self.images==None:
            print "DB not connected"
            return
        try:
            self.images.insert_one({"_id": file,"hash": hashes,"size_on_disk": size_on_disk,"image_size":size,"timestamp": timestamp})
        except pymongo.errors.DuplicateKeyError:
            print "Duplicate key:"

    def show(self):
        print "In show"
        if self.images==None:
            print "Empty"
            return
        total = self.images.count()
        pprint(list(self.images.find()))
        print("Total: {}".format(total))

    def delete(self,key="*",value="**"):
        try:
            self.images.remove({key:value})
            return True
        except:
            print "Failed to Delete"
            return False




    def get_image_file_from_path(self,path):
        path = os.path.abspath(path)
        print "path of images ",path
        images=[]
        for root, dirs, files in os.walk(path):
            for file in files:
                file = os.path.join(root, file)
                if self.img_processing.is_image(file):
                    images.append(file)
        return images

    def remove_image_from_db(self,file):  #here file is the id of the file
        self.delete("_id",file)

    def remove_images_from_path(self,path):
        files = self.get_image_file_from_path(path)
        for file in files:
            self.remove_image_from_db(file)

    def is_in_db(self,file_id):
        if self.images.count({"_id":file_id})>0:
            return True
        return False

    def reset_database(self):
        self.images.drop()

    def get_list_new_files(self,files):
        print "get List new files ",files
        if files==None or len(files)==0:
            return None
        new_list=[]
        for file in files:
            if self.is_in_db(file)==False:
                new_list.append(file)
        return new_list



    def get_file_size(self,file_name):
        try:
            return os.path.getsize(file_name)
        except:
            return 0

    def get_image_dim(self,img):
        return "{} x {}".format(*img.size)

    #https://stackoverflow.com/questions/23064549/get-date-and-time-when-photo-was-taken-from-exif-data-using-pil
    def get_timestamp(self,img):
        #tags = EXIF.process_file(img, stop_tag="EXIF DateTimeOriginal")
        #dateTaken = tags["EXIF DateTimeOriginal"]
        return time.time()


    def add_folder_path(self,path):
        print "Path ",path

        files = self.get_image_file_from_path(path)
        new_files=self.get_list_new_files(files)
        print "New files ",new_files
        for file_ in new_files:
            file, hashes, size_on_disk, size, timestamp = self.img_processing.hash_file(file_)
            self.add_image_to_database_with_hash(file, hashes, size_on_disk, size, timestamp)

    def __thread_poller__(self):
        self.hadoop_message_parser = Hadoop_Message_Parser()
        self.hadoop_message_parser.poll_continuously()

    def __thread_take_input__(self):
        while True:
            time.sleep(3)
            cmd = raw_input("")
            if cmd == "-1":
                break
            if cmd == "" or len(cmd) == 0:
                continue
            self.execute(cmd)

    def __thread_display_output_console__(self):
        self.hadoop_message_parser=Hadoop_Message_Parser()
        while True:
            time.sleep(10)
            print "Repeating "
            if self.hadoop_message_parser.repeat_images!=None and len(self.hadoop_message_parser.repeat_images)>0:
                print "Repeating Images "
                for image in self.hadoop_message_parser.repeat_images:
                    print image["_id"]



def main():
    print "Enter Command"
    print "duplicate_search -db <path>\n\n"
    finder = Finder()


    thread1 = threading.Thread(target=finder.__thread_poller__())

    thread2 = threading.Thread(target=finder.__thread_take_input__())

    #thread3 = threading.Thread(target=finder.__thread_display_output_console__())

    thread2.join()
    thread1.join()
    #thread3.join()
    print "Polling finished"


if __name__=="__main__":

    main()