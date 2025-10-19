import pymongo
import os

client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
cursor = client["unfreeze"]