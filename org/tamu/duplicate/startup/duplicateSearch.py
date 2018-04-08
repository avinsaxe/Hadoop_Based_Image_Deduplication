from docopt import docopt
from org.tamu.duplicate.startup.DBConnection import DBConnection
db_path=""

collection=DBConnection.connectMongo()

if __name__=="__main__":
    command=docopt(__docopt__)
    if command["-database"]:
        db_path=command["-database"]


