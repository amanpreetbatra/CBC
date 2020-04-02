from connection import *
from fatsecret import *
import json
from bson.objectid import ObjectId
from flask import redirect, url_for, session, request,jsonify
from datetime import date

fs = Fatsecret(consumer_key, consumer_secret)
import bcrypt

'''Returns a list of 20 search items corresponding to  name. If page is set to 0 it returns first 20 results , i.e: 1-20, and if it is set
to 1 the result list contain 21-40 and so on'''


def food_search(name, page):
    result = list(fs.foods_search(search_expression=name, page_number=page))

    data = []
    for i in range(len(result)):
        data.append({
            "food_description": result[i]["food_description"],
            "food_id": result[i]["food_id"],
            "food_name": result[i]["food_name"],
            "food_type": result[i]["food_type"]
        })

        x = list(food.find({"food_id": data[i]['food_id']}))
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
    response = fs.food_get(food_id)
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
        if x[0]['FLAG'] == 1:
            result = {"message": "Heartrate data found in database",
                      "flag": "1",
                      "heartrate": x[0]["HEARTRATE"]}


        else:
            result = {"message": "Heartrate data not found in database",
                      "flag": "0",
                      "heartrate": ""}
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
    return custom_food.remove({"_id": ObjectId(oid)})


def update_mealplan(oid, data):
    try:
        # insert into new collection
        custom_food.update({"_id": ObjectId(oid)}, data)
        x = {"message": "Successfully Updated Data"}
    except err.DuplicateKeyError:
        # skip document because it already exists in new collection
        print(err.DuplicateKeyError)
        x = {"message": "Failed"}
    return json.dumps(x)


def store_mealplan(data):
    insert = {"Brand": data["Brand"],
              "Brand_Type": data["Brand_Type"],
              "Prod_name": data["Prod_name"],
              "Calories": data["Calories"],
              "Proteins": data["Proteins"],
              "Fats": {"Total_fat": data["Fats"]["Total_fat"], "Saturated_fat": data["Fats"]["Saturated_fat"],
                       "Monounsaturated_fat": data["Fats"]["Monounsaturated_fat"],
                       "Polyunsaturated_fat": data["Fats"]["Polyunsaturated_fat"]
                       },
              "Carbohydrates": {"Total_carbs": data["Carbohydrates"]["Total_carbs"],
                                "Sugar": data["Carbohydrates"]["Sugar"]},
              "Fibers": data["Fibers"],
              "Energy": data["Energy"],
              "Sodium": data["Sodium"],
              "Cholesterol": data["Cholesterol"],
              "Potassium": data["Potassium"],
              "Prod_img": data["Prod_img"]}
    print(insert)
    try:
        # insert into new collection
        custom_food.insert(insert)
        x = {"message": "Successfully Inserted Data"}
    except err.DuplicateKeyError:
        # skip document because it already exists in new collection
        print(err.DuplicateKeyError)
        x = {"message": "Dublicate Entry"}
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


def login():
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if login_user["authorised"] == "true":
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('crm', _external=True))

    return 'Invalid username/password combination'


def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


def register(data):
    existing_user = users.find_one({'name': data['username']})

    if existing_user is None:
        hashpass = bcrypt.hashpw(data['pass'].encode('utf-8'), bcrypt.gensalt())
        users.insert(
            {'name': data['username'], 'password': hashpass, 'isadmin': 'false', 'authorised': 'false'})
        return redirect(url_for('index'))
    return 'That username already exists!'


def insert_hr(data):
    x = list(col.find({"EXERCISE": data["EXERCISE"],
                       "GENDER": data["GENDER"],
                       "LEVEL": data["LEVEL"],
                       "REPS": data["REPS"],
                       "AGE": data["AGE"],
                       "lift WEIGHT": data["lift WEIGHT"]
                       }))
    print(x[0])
    '''object id varible'''
    oid = x[0]['_id']
    if int(x[0]['FLAG']) == 0:
        user = col.update({"_id": ObjectId(oid)}, {
            "EXERCISE": data["EXERCISE"],
            "GENDER": data["GENDER"],
            "LEVEL": data["LEVEL"],
            "REPS": data["REPS"],
            "AGE": data["AGE"],
            "lift WEIGHT": data["lift WEIGHT"],
            "HEARTRATE": data["HEARTRATE"],
            "FLAG": "1"
        })
        message = {"message": "DATABASE UPDATED "}
        return json.dumps(message)

    else:
        message = {"message": "NOT REQUIRED! ALREADY FILLED"}
        return json.dumps(message)


def insert_weight(data):
    query = weight.find_one({"Phone" : data["Phone"]})

    if query is None:
        dd = str(date.today())
        inse = weight.insert_one({
            "name": data["Name"],
            "Phone": data["Phone"],
            "weights": [
                {
                    "date": dd ,
                    "weight": data["Weight"]
                }]

        })
    else:
        u = []
        count = 0
        for m in query["weights"]:
            if m["date"] == str(date.today()):
                m["weight"]= data["Weight"]
                u.append(m)
                count = 1
                break
            u.append(m)
        if count!=1:
            u.append({'date': str(date.today()), 'weight': data["Weight"]})
            print(u)
        inse = weight.update({"_id": ObjectId(query["_id"])}, { "$set": { "weights": u } })
    inse = str(inse)
    return jsonify({"message":"Successfully Updated"})


def return_weight(data):
    my_query = {"Phone": data["Phone"]}
    find_query = weight.find_one(my_query)
    if find_query is  None:
        return jsonify({"message":"No Data"}),403
    else:
        return jsonify({"Name": find_query["name"],"Phone": find_query["Phone"], "weights" : find_query["weights"][-30:]})