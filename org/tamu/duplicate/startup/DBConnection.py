import pymongo
import DB_Constants
import os

def connect():
    url="mongodb://"+DB_Constants.host+"/"+DB_Constants.db
    client = pymongo.MongoClient(url)
    db = client[DB_Constants.db]
    collection = db[DB_Constants.collection]
    return collection

def connect_db(db_path="mongodb://"+DB_Constants.host+"/"+DB_Constants.db):
    #check if path is a mongo host
    if 'mongodb://'==db_path[:10]:
        client = pymongo.MongoClient(db_path)
        print ("Connected server...")
        db = client[DB_Constants.db]
        collection = db[DB_Constants.collection]

    # If this is not a URI
