import pymongo

'''Fatsecret Keys'''
consumer_key = 'f02034d0d7b24cb594f5c65f9fa525dd'
consumer_secret = 'f5fac6873b544b5191809b5ee7f9b6fc'
'''----------'''


'''Mongo connection'''
mongo = pymongo.MongoClient('mongodb+srv://naman:naman1234@cluster0-t91dz.mongodb.net/test', maxPoolSize=50, connect=False)
'''------------'''

'''MongoDb Database and collections'''
db = pymongo.database.Database(mongo, 'VITRADA')
db1 = pymongo.database.Database(mongo, 'CALINDA')
db2 = pymongo.database.Database(mongo, 'CALINFO')
login_db= pymongo.database.Database(mongo, 'Login')
col = pymongo.collection.Collection(db, 'cbcavg')
food = pymongo.collection.Collection(db1, 'CIfood')
nutri = pymongo.collection.Collection(db1, 'CBnutri')
custom_food =pymongo.collection.Collection(db1, 'CICustomfood')
users =pymongo.collection.Collection(login_db, 'user')
weight = pymongo.collection.Collection(db2, 'Cinsight')


custom_food.create_index(
    [("Product-name", pymongo.DESCENDING), ("Brand", pymongo.ASCENDING),("Brand-Type", pymongo.ASCENDING)], unique=True)

users.create_index([("name", pymongo.ASCENDING)],unique=True)
'''------------------'''
err = pymongo.errors