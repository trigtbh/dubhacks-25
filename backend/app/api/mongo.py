import pymongo
from app.config import settings

if settings.mongodb_uri:
    client = pymongo.MongoClient(settings.mongodb_uri)
    cursor = client.unfreeze
else:
    client = None
    cursor = None
