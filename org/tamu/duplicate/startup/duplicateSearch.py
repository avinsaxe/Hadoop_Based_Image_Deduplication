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
import imagehash
import magic
from pprint import pprint



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

        pprint (self.images)


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
            elif len(command_list)==3:
                if command_list[1]=="-add":
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


    def is_image(self,file_name):
        supported = ['jp2', 'jpeg', 'gif', 'png','pcx', 'tiff', 'x-ms-bmp', 'x-portable-pixmap', 'x-xbitmap']
        try:
            mime = magic.from_file(file_name, mime=True)
            mime.rsplit('/', 1)[1] in supported
            return True
        except IndexError:
            return False

    def get_image_file_from_path(self,path):
        path = os.path.abspath(path)
        print "path of images ",path
        images=[]
        for root, dirs, files in os.walk(path):
            for file in files:
                file = os.path.join(root, file)
                if self.is_image(file):
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


    def hash_file(self,file):
        hashes = []
        print "Image file ",file
        try:
            curr_image = Image.open(file)

            # 0 degree hash
            hashes.append(str(imagehash.phash(curr_image)))

            # 90 degree hash
            curr_image = curr_image.rotate(90, expand=True)
            hashes.append(str(imagehash.phash(curr_image)))

            # 180 degree hash
            curr_image = curr_image.rotate(90, expand=True)
            hashes.append(str(imagehash.phash(curr_image)))

            # 270 degree hash
            curr_image = curr_image.rotate(90, expand=True)
            hashes.append(str(imagehash.phash(curr_image)))

            # flip and hash
            rotated_image = curr_image.transpose(Image.FLIP_LEFT_RIGHT)
            hashes.append(str(imagehash.phash(rotated_image)))

            hashes = ''.join(sorted(hashes))

            size_on_disk = self.get_file_size(curr_image)
            size = self.get_image_dim(curr_image)
            timestamp = self.get_timestamp(curr_image)

            return file, hashes, size_on_disk, size, timestamp

        except OSError:
            print "Unable to open ",file
            return None

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
            file, hashes, size_on_disk, size, timestamp = self.hash_file(file_)
            self.add_image_to_database_with_hash(file, hashes, size_on_disk, size, timestamp)





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