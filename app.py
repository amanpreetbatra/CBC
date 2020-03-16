from flask import Flask, request,render_template
from bson.objectid import ObjectId
from connection  import  *
import json
import views as v
import sys


app = Flask(__name__)


''' THIS IS THE SEARCH API WHICH TAKES TWO INPUTS 1. Search String 2. Page Number'''
@app.route('/foodsearch', methods= ['POST'])
def food_s():
    data = json.loads(request.data)
    try:
        return v.food_search(data['data'], data['page'])
    except:
        e = sys.exc_info()[0:2]
        dat = {"message" : str(e) }

        return json.dumps(dat)


'''API TO GET NUTRITIONAL VALUES OF A PARTICULAR FOOD ID'''
@app.route('/get_nut', methods= ['POST'])
def food_g():
    data = json.loads(request.data)
    try:
        return v.nutri_facts(data['food_id'])
    except:
        e = sys.exc_info()[0:2]
        dat = {"message": str(e)}

        return json.dumps(dat)

'''API TO SEND HEARTRATE TO FRONTEND IF IT IS AVAILABLE IN BACKEND'''
@app.route('/op_hr', methods= ['POST'])
def fetch_heart():
    data = json.loads(request.data)
    return v.fetch_heartrate(data)


@app.route('/customfoodins', methods= ['POST'])
def custom_meal():
    data = json.loads(request.data)
    return v.store_mealplan(data)


@app.route('/inp_insight', methods= ['POST'])
def insights():
    data = json.loads(request.data)
    return v.store_insights(data)



@app.route('/in_hr', methods= [ 'POST'])
def insert_hr():
    if request.method == 'POST':
        data = json.loads(request.data)
        x = list(col.find({"EXERCISE": data["EXERCISE"],
            "GENDER": data["GENDER"],
            "LEVEL": data["LEVEL"],
            "REPS":data["REPS"],
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
                "REPS":data["REPS"],
                "AGE": data["AGE"],
                "lift WEIGHT": data["lift WEIGHT"],
                "HEARTRATE": data["HEARTRATE"],
                "FLAG" : "1"
                })
            message ={"message": "DATABASE UPDATED "}
            return json.dumps(message)

        else:
            message = { "message": "NOT REQUIRED! ALREADY FILLED" }
            return json.dumps(message)


@app.route('/crm', methods= [ 'GET'])
def crm():
    data = list(v.show_mealplan())
    return render_template("crm.html", data=data)

@app.route('/getmealplan', methods= [ 'POST'])
def crm_1():
    data = json.loads(request.data)

    response = list(v.get_mealplan(data["id"]))
    response[0]["_id"] = str(response[0]["_id"])

    response = json.dumps(response)
    return response

@app.route('/storemealplan', methods= [ 'POST'])
def storemealplan():
    data = request.form.to_dict()

    inp = v.custom_json(data)
    print(inp)

    return v.store_mealplan(inp)

@app.route('/delmealplan', methods= [ 'POST'])
def delmealplan():
    data = json.loads(request.data)

    response = list(v.delete_mealplan(data["id"]))
    print(response)
    return 'ok'

@app.route('/updatemealplan', methods= [ 'POST'])
def updatemealplan():
    data = request.form.to_dict()

    inp = v.custom_json(data)
    print(inp)

    return v.update_mealplan(data['_id'], inp)


if __name__ == '__main__':
    app.run()
