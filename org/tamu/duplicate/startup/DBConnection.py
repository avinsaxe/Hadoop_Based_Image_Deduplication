import pymongo
import DB_Constants

class DBConnection:
    def connect(self):
        self.url="mongodb://"+DB_Constants.host+"/"+DB_Constants.db
        client = pymongo.MongoClient(url)
        db = client[DB_Constants.db]
        collection = db[DB_Constants.collection]
        return collection
