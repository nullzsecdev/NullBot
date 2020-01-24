import pymongo

client = None
db = None

def connect(connection_string, database_name):
    global client, db
    client = pymongo.MongoClient(connection_string)
    db = client[database_name]
    return db