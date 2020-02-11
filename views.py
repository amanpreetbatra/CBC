from connection  import  *
from fatsecret import *
import json

def food_search(name):
    y = food.create_index([('food_name', 'text')])

    fs = Fatsecret(consumer_key, consumer_secret)
    home_db = list(food.find({"$text": {"$search": str(name) }}))

    if len(home_db) == 0:
        result = list( fs.foods_search(name))
        for i in range(len(result)):
            del result[i]['_id']

        y = food.insert(list(result))
        print(result)
        return json.dumps(result)
    else :
        for i in range(len(home_db)):
            del home_db[i]['_id']
        result = json.dumps(home_db)
        print(result)
        return result



    #x = food.insert(result)
    # print(home_db)
    # return 'hello'

