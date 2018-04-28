import os
import time
from flask_cors import CORS
from jinja2 import FileSystemLoader, Environment
from more_itertools import chunked
from PIL import Image, ExifTags
import pymongo
import DBConnection
import Constants
import magic
from pprint import pprint
from difflib import SequenceMatcher
import sdhash

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

from PIL import Image,ImageTk

class ImageProcessing:
    def __init__(self):
        self.similarity_threshold=0.4
        self.root= Tk()
        self.root.title("Image UI")

    def get_image_dim(self,img):
        return "{} x {}".format(*img.size)

    def get_file_size(self,file_name):
        try:
            return os.path.getsize(file_name)
        except:
            return 0

    def display_image(self,path):
        im = Image.open(path)  # This is the correct location and spelling for my image location
        photo = ImageTk.PhotoImage(im)
        cv = Canvas()
        cv.pack(side='top', fill='both', expand='yes')
        cv.create_image(10, 10, image=photo, anchor='nw')
        mainloop()

    def get_timestamp(self, img):
        # tags = EXIF.process_file(img, stop_tag="EXIF DateTimeOriginal")
        # dateTaken = tags["EXIF DateTimeOriginal"]
        return time.time()

    def is_image(self, file_name):
        supported = ['jp2', 'jpeg', 'gif', 'png', 'pcx', 'tiff', 'x-ms-bmp', 'x-portable-pixmap', 'x-xbitmap']
        try:
            mime = magic.from_file(file_name, mime=True)
            mime.rsplit('/', 1)[1] in supported
            return True
        except IndexError:
            return False

    def hash_file(self,file):
        hashes = []
        print "Image file ",file
        h = sdhash.Hash()

        try:
            curr_image = Image.open(file)

            # 0 degree hash
            hashes.append(str(h.hash_image(curr_image)))

            # 90 degree hash
            curr_image = curr_image.rotate(90, expand=True)
            hashes.append(str(h.hash_image(curr_image)))

            # 180 degree hash
            curr_image = curr_image.rotate(90, expand=True)
            hashes.append(str(h.hash_image(curr_image)))

            # 270 degree hash
            curr_image = curr_image.rotate(90, expand=True)
            hashes.append(str(h.hash_image(curr_image)))

            # flip and hash
            #rotated_image = curr_image.transpose(Image.FLIP_LEFT_RIGHT)
            #hashes.append(str(imagehash.phash(rotated_image)))

            hashes = ''.join(sorted(hashes))

            size_on_disk = self.get_file_size(curr_image)
            size = self.get_image_dim(curr_image)
            timestamp = self.get_timestamp(curr_image)

            return file, hashes, size_on_disk, size, timestamp

        except OSError:
            print "Unable to open ",file
            return None


    def find_similarity(self,hash1,hash2):
        return SequenceMatcher(None, hash1, hash2).ratio()

    def are_images_similar(self,hash1,hash2):
        ratio=self.find_similarity(hash1,hash2)
        print ratio
        if ratio>self.similarity_threshold:
            return True
        else:
            return False