from connection  import  *
from fatsecret import *
import json
from bson.objectid import ObjectId
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

    print(x)
    if len(x) != 0:
        if x[0]['FLAG'] == 1 :
            result = {"message": "Heartrate data found in database",
                      "flag": "1",
                      "heartrate": x[0]["HEARTRATE"]}


        else:
            result = {"message": "Heartrate data not found in database",
                  "flag" : "0",
                  "heartrate" : ""}
    else:
        result = {"message": "Heartrate data not found in database",
                  "flag": "0",
                  "heartrate": ""}
    return json.dumps(result)


def show_mealplan():
    return custom_food.find()


def get_mealplan(oid):
    return custom_food.find({"_id": ObjectId(oid)})

def delete_mealplan(oid):
    return  custom_food.remove({"_id": ObjectId(oid)})


def update_mealplan(oid, data):
    try:
        # insert into new collection
        custom_food.update({"_id": ObjectId(oid)}, data)
        x = {"message":"Successfully Updated Data"}
    except err.DuplicateKeyError:
        # skip document because it already exists in new collection
        print(err.DuplicateKeyError)
        x = {"message":"Failed"}
    return json.dumps(x)



def store_mealplan(data):
    insert = { "Brand" : data["Brand"],
               "Brand_Type": data["Brand_Type"],
               "Prod_name": data["Prod_name"],
               "Calories": data["Calories"],
               "Proteins": data["Proteins"],
               "Fats":{ "Total_fat": data["Fats"]["Total_fat"],"Saturated_fat": data["Fats"]["Saturated_fat"],
                         "Monounsaturated_fat": data["Fats"]["Monounsaturated_fat"],
                         "Polyunsaturated_fat": data["Fats"]["Polyunsaturated_fat"]
                        },
               "Carbohydrates": {"Total_carbs" : data["Carbohydrates"]["Total_carbs"],
               "Sugar":data["Carbohydrates"]["Sugar"]},
               "Fibers": data["Fibers"],
               "Energy" : data["Energy"],
               "Sodium": data["Sodium"],
               "Cholesterol": data["Cholesterol"],
               "Potassium": data["Potassium"],
               "Prod_img": data["Prod_img"]}
    print(insert)
    try:
        # insert into new collection
        custom_food.insert(insert)
        x = {"message":"Successfully Inserted Data"}
    except err.DuplicateKeyError:
        # skip document because it already exists in new collection
        print(err.DuplicateKeyError)
        x = {"message":"Dublicate Entry"}
    return json.dumps(x)

def store_insights(data):
    return "hello"

def custom_json(data):
   imp = {"Brand": data["brand1"],
     "Brand_Type": data["brand_type1"],
     "Prod_name": data["product_name1"],
     "Calories": data["calories1"],
     "Proteins": data["proteins1"],
     "Fats": {"Total_fat": data["total_fat1"], "Saturated_fat": data["saturated1"],
              "Monounsaturated_fat": data["monosaturated1"],
              "Polyunsaturated_fat": data["polysaturated1"]
              },
     "Carbohydrates": {"Total_carbs": data["total_carbs1"],
                       "Sugar": data["sugar1"]},
     "Fibers": data["fibers1"],
     "Energy": data["energy1"],
     "Sodium": data["sodium1"],
     "Cholesterol": data["cholesterol1"],
     "Potassium": data["potassium1"],
     "Prod_img": data["prod_img"]}

   return imp

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS