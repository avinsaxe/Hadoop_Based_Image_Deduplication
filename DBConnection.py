import pymongo
import Constants
import os

def connect():
    url="mongodb://" + Constants.host + "/" + Constants.db
    client = pymongo.MongoClient(url)
    db = client[Constants.db]
    return db

def connect_db(db_path="mongodb://" + Constants.host + "/" + Constants.db):
    #check if path is a mongo host
    if 'mongodb://'==db_path[:10]:
        client = pymongo.MongoClient(db_path)
        print ("Connected server...")
        db = client[Constants.db]
        return db

    # If this is not a URI
