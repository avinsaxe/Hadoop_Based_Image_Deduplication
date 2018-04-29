import json
import os
class OuputCreator:
    def __init__(self,map_file='/home/hduser/CloudComputing/CSCE689_Project2/ImageCounter/new_data.txt',image_profiles='output/image_profiles.json'):
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
        self.hash_file.close()

    def write_hashes(self,hashes_data=[],mode="w+"):
        print hashes_data
        if hashes_data==None or len(hashes_data)==0:
            return
        try:
            self.hash_file = open(self.hashes, "w+")
        except:
            print "Error opening file ", self.hashes
            return


        for i in range(0,len(hashes_data)):
            if i==0 :
                self.hash_file.write(hashes_data[i]+"\n")
                self.hash_file.close()
                self.hash_file=None
            elif self.hash_file==None:
                try:
                    self.hash_file = open(self.hashes, "a+")
                except:
                    print "Error opening file ", self.hashes
                    return
                self.hash_file.write(hashes_data[i] + "\n")
        if self.hash_file!=None:
            self.hash_file.close()

    def write_json(self,jsonData="",mode="w+"):
        if jsonData=="":
            return

        try:
            self.image_profile_file = open(self.image_profiles, mode)
        except:
            print "Error opening file ", self.image_profiles

        json.dump(jsonData,self.image_profile_file)
        #self.image_profile_file.write(jsonData)





