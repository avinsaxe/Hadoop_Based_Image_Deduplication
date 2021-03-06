import DBConnection
import os
from pprint import pprint
import re
from time import sleep
import Constants
import time
from threading import Thread



class ImageShow:
    def __init__(self):
        self.path="index.html"
        self.images_file="duplicate_images_path.txt"
        self.hadoop_out='output/hadoop_output.txt'
        self.images_html_text=''
        self.hadoop_in='input/hashes.txt'

    def get_collection(self):
        if self.db == None:
            self.db = DBConnection.connect()
        collection = self.db[Constants.collection]
        return collection

    def setup_db(self, db_path=''):
        self.db_path = db_path
        if db_path == "":
            self.db = DBConnection.connect()
            self.images = self.get_collection()
        else:
            self.db = DBConnection.connect_db(db_path)
            self.images = self.get_collection()
        pprint(self.images)

        #pprint (self.images)
    def __reset_dup_images_paths__(self):
        f=open(self.images_file,'w')
        f.write("")
        f.close()
    def write_to_html(self):
        f = open(self.path, 'w')
        message = """<html>
        <head>
        <script>
            function toCelsius(f) {
               return (5/9) * (f-32);
            }
            function delete_file(file_name){
                var r = confirm("Go to the path "+file_name +" and delete");
                if(r == true)
                {
                    
                }
            }

        </script>
        </head>
        <body><h1>Duplicate Images. Pick and Delete </h1>"""+self.images_html_text+"""</body></html>"""
        self.images_html_text=""
        f.write(message)
        f.close()


    def get_content_from_file(self):
        f=open(self.images_file,'r')
        image_path=''
        cnt=0

        for line in f.readlines():
            line=line.strip("\n")
            image_path="""<a href="" ><img src='"""+line+"""' width="400" height="400"/> </a>"""
            button= '<input type="button" id="buttonId'+str(cnt)+'" ' +'name="'+line+'" value="'+'Delete"' +""" onclick="delete_file('"""+line+""" ');"/>"""
            self.images_html_text=self.images_html_text+image_path+button
            cnt=cnt+1




    def split_multiple_spaces(self, l=""):
            if l == "":
                return None
            splits = re.split(r'\s{1,}', l)
            splits = [i for i in splits if i != '']
            return splits

    def get_image_from_hash(self,hash=""):
        if self.images==None:
            self.setup_db()
        if self.images==None:
            return None
        all_files=[]
        all_images = self.images.find()
        for image in all_images:
            if image["hash"]==hash:
                all_files.append(image)
        return all_files

    #Reads hadoop output file, checks for count>1 and extracts image paths from such hashes to add to the file duplicate_images_path.txt
    def write_duplicate_image_paths_to_file(self):
        self.__reset_dup_images_paths__()
        f=open(self.hadoop_out,'r')
        for line in f.readlines():
            splits=self.split_multiple_spaces(line)
            if len(splits)!=2:
                continue
            hash=splits[0]
            count=int(splits[1])
            #print hash,"  ", count
            if count>1:
                img_list=self.get_image_from_hash(hash)
                #print img_list
                if img_list==None or len(img_list)==0:
                    continue
                f1 = open(self.images_file, "a+")
                for k in range(0,len(img_list)):
                    f1.write(img_list[k]["_id"]+"\n")
                f1.close()
        f.close()





def main():
    imageshow=ImageShow()
    imageshow.setup_db()
    print "Updating HTML file...Every 10 seconds"
    while True:
        imageshow.write_duplicate_image_paths_to_file()
        imageshow.get_content_from_file()
        imageshow.write_to_html()
        time.sleep(10)

if __name__=="__main__":
    main()
