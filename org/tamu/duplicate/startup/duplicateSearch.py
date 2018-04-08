"""
"""
import os

from flask_cors import CORS
import imagehash
from jinja2 import FileSystemLoader, Environment
from more_itertools import chunked
from PIL import Image, ExifTags
import pymongo
import DBConnection

class Finder:
    def __init__(self):
        self.db_path=""
        self.images=None

    def setup_db(self,db_path):
        self.db_path=db_path
        if db_path=="":
            images=DBConnection.connect()
        else:
            images=DBConnection.connect_db(db_path)

        print images


    def execute(self,command=""):
        if command=="":
            return
        command_list=command.split(" ")
        if len(command_list)==3 and command_list[0]=="find" and command_list[1]=="-db":
            db_path=command_list[2]
            if db_path=="default":
                self.setup_db("")
            else:
                self.setup_db(db_path)








def main():
    print "Enter Command"
    print "find -db <path>\n\n"
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