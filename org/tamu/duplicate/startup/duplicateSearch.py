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
from org.tamu.duplicate.startup import Constants
import Constants




class Finder:
    def __init__(self):
        self.db_path=""
        self.images=None

    def setup_db(self,db_path):
        self.db_path=db_path
        if db_path=="":
            self.images=DBConnection.connect()
        else:
            self.images=DBConnection.connect_db(db_path)

        print self.images


    def execute(self,command=""):
        if command=="":
            return
        command_list=command.split(" ")
        if len(command_list)>1 and command_list[0]==Constants.command_start:
            if len(command_list)==3 and command_list[1]=="-db":
                db_path=command_list[2]
                if db_path=="default":
                    self.setup_db("")
                else:
                    self.setup_db(db_path)
            elif len(command_list)==3 and command_list[1]=="-add":
                folder_path=command_list[2]
                if folder_path=="":
                    print "Empty folder"
                    return
                else:
                    self.add_image_to_database_with_hash("id1","#id1",10,time.time())
            elif len(command_list)==2 and command_list[1]=="-show":
                self.show()
            elif len(command_list)==4 and command_list[1]=="-delete":
                delete_key=command_list[2]
                delete_value=command_list[3]
                self.delete(delete_key,delete_value)

    def add_image_to_database_with_hash(self,file_id,hash,size,timestamp):
        if self.images==None:
            print "DB not connected"
            return
        try:
            self.images.insert_one({"_id": file_id,"hash": hash,"size": size,"timestamp": timestamp})
        except pymongo.errors.DuplicateKeyError:
            print "Duplicate key:"

    def show(self):
        print "In show"
        total = self.images.count()
        print(list(self.images.find()))
        print("Total: {}".format(total))

    def delete(self,key="*",value="**"):
        self.images.remove({key:value});




def main():
    print "Enter Command"
    print "duplicate_search -db <path>\n\n"
    finder=Finder()
    while True:
        cmd = raw_input("")
        if cmd == "-1":
            break
        if cmd == "" or len(cmd) == 0:
            continue
        finder.execute(cmd)




if __name__=="__main__":
    main()