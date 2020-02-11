import pymongo

'''Fatsecret Keys'''
consumer_key = 'f02034d0d7b24cb594f5c65f9fa525dd'
consumer_secret = 'f5fac6873b544b5191809b5ee7f9b6fc'
'''----------'''


'''Mongo connection'''
mongo = pymongo.MongoClient('mongodb+srv://naman:naman1234@cluster0-t91dz.mongodb.net/test', maxPoolSize=50, connect=False)
'''------------'''

'''MongoDb Database and collections'''
db = pymongo.database.Database(mongo, 'cbc')
col = pymongo.collection.Collection(db, 'cbcavg')
food = pymongo.collection.Collection(db, 'cbcfood')
'''------------------'''
