from connection  import  *
from fatsecret import *
import json

def food_search(name):
    y = food.create_index([('food_name', 'text')])

    fs = Fatsecret(consumer_key, consumer_secret)
    #home_db = list(food.find({"$text": {"$search": str(name) }}))

    #if len(home_db) == 0:
    result = list( fs.foods_search(name))
    print(result)
    data = [{ "food_description": "", "food_id": "", "food_name":"" , "food_type": ""}] * len(result)
    for i in range(len(result)):
        data[i]["food_description"] = result[i]["food_description"]
        data[i]["food_id"] = result[i]["food_id"]
        data[i]["food_name"] = result[i]["food_name"]
        data[i]["food_type"] = result[i]["food_type"]
    print(data)
    home_db = list(food.find({"$text": {"$search": str(name) }}))

    for i in range(len(result)):
        if len(list(food.find({"food_id":data[i]['food_id']}))) == 0:
            y = food.insert(list(result[i]))
        else:
            pass
    #if len(home_db) == 0:
        #y = food.insert(list(result)) # Data is inserted in CALINDA DB CIfood (Data Validation for new search{duplication},  Hit own db if data present)
    data =json.dumps(data)
    return data
    # else :`
    #     for i in range(len(home_db)):
    #         del home_db[i]['_id']
    #     result = json.dumps(home_db)
    #     print(result)
    #     return result



    #x = food.insert(result)
    # print(home_db)
    # return 'hello'

