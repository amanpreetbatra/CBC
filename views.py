from connection  import  *
from fatsecret import *
import json
fs = Fatsecret(consumer_key, consumer_secret)

'''Returns a list of 20 search items corresponding to  name. If page is set to 0 it returns first 20 results , i.e: 1-20, and if it is set
to 1 the result list contain 21-40 and so on'''
def food_search(name, page):
    result = list(fs.foods_search(search_expression=name, page_number=page))
    
    data = []
    for i in range(len(result)):
        data.append({
            "food_description" : result[i]["food_description"],
            "food_id"   :  result[i]["food_id"],
            "food_name" :  result[i]["food_name"],
            "food_type" :  result[i]["food_type"]
                    })

        x = list(food.find({"food_id":data[i]['food_id']}))
        if len(x) == 0:
            # print(data[i])
            try:
                # insert into new collection
                y = food.insert(data[i])
            except err.DuplicateKeyError:
                # skip document because it already exists in new collection
                continue

    for i in range(len(data)):
        if "_id" in data[i].keys():
            del data[i]["_id"]
    print("Final Data:", data)
    data = json.dumps(data)
    return data


''' Returns all the Nutritional values of a particular food id that is inserted'''
def nutri_facts(food_id):
    response =fs.food_get(food_id)
    x = list(nutri.find({"food_id": response['food_id']}))
    if len(x) == 0:
        try:
            # insert into new collection
            nutri.insert(response)
        except err.DuplicateKeyError:
            # skip document because it already exists in new collection
            print(err.DuplicateKeyError)
    else:
        print("alredy in db")

    return response


def fetch_heartrate(data):
    x = list(col.find({"EXERCISE": data["EXERCISE"],
                       "GENDER": data["GENDER"],
                       "LEVEL": data["LEVEL"],
                       "REPS": data["REPS"],
                       "AGE": data["AGE"],
                       "lift WEIGHT": data["lift WEIGHT"]
                       }))
    oid = x[0]['_id']
    if x[0]['flag'] == 1:
        result = {"message": "Heartrate data found in database",
                  "flag": "1",
                  "heartrate": x[0]["HEARTRATE"]}

    else:
        result = {"message": "Heartrate data not found in database",
                  "flag" : "0",
                  "heartrate" : ""}
    return json.dumps(result)


def store_mealplan(data):
    insert = { "Brand" : data["Brand"],
               "Brand-Type": data["Brand-Type"],
               "Prod-name": data["Prod-name"],
               "Calories": data["Calories"],
               "Proteins": data["Proteins"],
               "Fats": data["Fats"],
               "Carbohydrates": data["Carbohydrates"],
               "Fibers": data["Fibers"] }
    print(insert)
    try:
        # insert into new collection
        custom_food.insert(insert)
        x = "Successfully Inserted Data"
    except err.DuplicateKeyError:
        # skip document because it already exists in new collection
        print(err.DuplicateKeyError)
        x = "Dublicate Entry"
    return x

def store_insights(data):
    return "hello"