import DBConnection
import os
from pprint import pprint
import re

class ImageShow:
    def __init__(self):
        self.path="index.html"
        self.images_file="duplicate_images_path.txt"
        self.hadoop_out='output/hadoop_output.txt'
        self.images_html_text=''

    def setup_db(self,db_path=''):
        self.db_path=db_path
        if db_path=="":
            self.images= DBConnection.connect()
        else:
            self.images= DBConnection.connect_db(db_path)

        pprint (self.images)
    def __reset_dup_images_paths__(self):
        f=open(self.images_file,'w')
        f.write("")
        f.close()
    def write_to_html(self):
        f = open(self.path, 'w')
        message = """<html>
        <head></head>
        <body><p>Duplicate Images. Pick and Delete <p>"""+self.images_html_text+"""</body></html>"""
        f.write(message)
        f.close()
        self.__reset_dup_images_paths__()

    def get_content_from_file(self):
        f=open(self.images_file,'r')
        image_path=''
        for line in f.readlines():
            image_path="""<img src='"""+line+"""' width="400" height="400"/>"""
            self.images_html_text=self.images_html_text+image_path
            print self.images_html_text

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
        all_images = self.images.find()
        for image in all_images:
            if image["hash"]==hash:
                return image
        return None

    #Reads hadoop output file, checks for count>1 and extracts image paths from such hashes to add to the file duplicate_images_path.txt
    def write_duplicate_image_paths_to_file(self):
        f=open(self.hadoop_out,'r')
        for line in f.readlines():
            splits=self.split_multiple_spaces(line)
            if len(splits)!=2:
                continue
            hash=splits[0]
            count=int(splits[1])
            print hash,"  ", count
            if count>1:
                img=self.get_image_from_hash(hash)
                print img
                if img==None:
                    continue

                f1=open(self.images_file,"a+")
                f1.write(img["_id"]+"\n")
                f1.close()
        f.close()





def main():
    imageshow=ImageShow()
    imageshow.setup_db()
    imageshow.write_duplicate_image_paths_to_file()

    imageshow.get_content_from_file()
    imageshow.write_to_html()

if __name__=="__main__":
    main()
