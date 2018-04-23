import json
import os
class OuputCreator:
    def __init__(self,map_file='output/hashes.txt',image_profiles='output/image_profiles.json'):
        self.hashes=map_file
        self.image_profiles=image_profiles
        self.hash_file=None
        self.image_profile_file=None

    def _open_file(self,file_path,mode="a+"):
        file=None
        try:
            file=open(file_path,mode)
        except:
            print "Error opening file ",file_path

        return file


    def write_line(self,hash=""):
        if hash=="":
            return
        if self.hash_file==None:
            self.hash_file=self._open_file(self.hashes,"a+")

        self.hash_file.write(hash)

    def write_hashes(self,hashes_data=[],mode="w+"):
        if hashes_data==None or len(hashes_data)==0:
            return
        try:
            self.hash_file = open(self.hashes, mode)
        except:
            print "Error opening file ", self.hashes


        for i in range(0,len(hashes_data)):
            self.hash_file.write(hashes_data[i]+"\n")

        self.hash_file.close()




