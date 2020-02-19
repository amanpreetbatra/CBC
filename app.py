from flask import Flask, request
from bson.objectid import ObjectId
from connection  import  *
import json
from views import  food_search


app = Flask(__name__)


''' THIS IS THE SEARCH API WHICH TAKES TWO INPUTS 1. Search String 2. Page Number'''
@app.route('/foodsearch', methods= ['POST'])
def food_s():
    x = json.loads(request.data)
    return food_search(x['data'], x['page'])


@app.route('/op_hr', methods= ['POST'])
def fetch_heart():
    if request.method=='POST':
        data = json.loads(request.data)
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
                      "heartrate":x[0]["HEARTRATE"]}

        else:
            result = {"message": "Heartrate data not found in database"}
        return json.dumps(result)




@app.route('/in_hr', methods= [ 'POST'])
def API():
    if request.method == 'GET':
        # x = list(col.find({"_id": ObjectId("5e388991272e4c23e056d732")}))
        # oid = x[0]['_id']
        # user = col.update({"_id": ObjectId(oid)}, {
        #
        #     "EXERCISE": "PUSHUP",
        #     "GENDER": "MALE",
        #     "LEVEL": "BEGINNER",
        #     "REPS": "LOW",
        #     "AGE": "A",
        #     "lift WEIGHT": "HEAVY",
        #     "HEARTRATE": "NULL",
        #     "PID": "1"
        # })
        # print(user)
        return 'hello'

    if request.method == 'POST':
        data = json.loads(request.data)
        x = list(col.find({"EXERCISE": data["EXERCISE"],
            "GENDER": data["GENDER"],
            "LEVEL": data["LEVEL"],
            "REPS":data["REPS"],
            "AGE": data["AGE"],
            "lift WEIGHT": data["lift WEIGHT"]
            }))

        '''object id varible'''
        oid = x[0]['_id']
        if x[0]['flag'] == 0:
            user = col.update({"_id": ObjectId(oid)}, {
                "EXERCISE": data["EXERCISE"],
                "GENDER": data["GENDER"],
                "LEVEL": data["LEVEL"],
                "REPS":data["REPS"],
                "AGE": data["AGE"],
                "lift WEIGHT": data["lift WEIGHT"],
                "HEARTRATE": data["HEARTRATE"],
                "PID": x[0]["PID"]
                })
            message = "DATABASE UPDATED "
            return json.dumps(message)

        else:
            message = "NOT REQUIRED! ALREADY FILLED"
            return json.dumps(message)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='80')
