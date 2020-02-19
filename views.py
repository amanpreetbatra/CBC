from connection  import  *
from fatsecret import *
import json

def food_search(name, page):
    y = food.create_index([('food_name', 'text')])

    fs = Fatsecret(consumer_key, consumer_secret)
    #home_db = list(food.find({"$text": {"$search": str(name) }}))

    #if len(home_db) == 0:
    result = list(fs.foods_search(search_expression=name, page_number=page))
    
    data = []
    #data = [""] * len(result)
   # data = [{ "food_description": "", "food_id": "", "food_name":"" , "food_type": ""}] * len(result)
    for i in range(len(result)):
        data.append({
            "food_description" : result[i]["food_description"],
            "food_id"   :  result[i]["food_id"],
            "food_name" :  result[i]["food_name"],
            "food_type" :  result[i]["food_type"] })


        x = list(food.find({"food_id":data[i]['food_id']}))
        # print ("length of x",len(x))
        if len(x) == 0:
            # print(data[i])
            try:
                # insert into new collection
                y = food.insert(data[i])
            except err.DuplicateKeyError:
                # skip document because it already exists in new collection
                continue

    # home_db = list(food.find({"$text": {"$search": str(name) }}))

    for i in range(len(data)):
        if "_id" in data[i].keys():
            del data[i]["_id"]
    print("Final Data:", data)
    data = json.dumps(data)
    return data

