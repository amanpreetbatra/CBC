import pymongo

mongo = pymongo.MongoClient('mongodb+srv://naman:naman1234@cluster0-t91dz.mongodb.net/test', maxPoolSize=50, connect=False)

db = pymongo.database.Database(mongo, 'cbc')
col = pymongo.collection.Collection(db, 'cbcavg')

