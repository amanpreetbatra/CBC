from flask import Flask, request
from bson.objectid import ObjectId
from connection  import  *
import json
from fatsecret import *

app = Flask(__name__)


@app.route('/hello', methods= ['GET', 'POST'])
def COLLECT_AVERAGE():
    if request.method == 'GET':
        consumer_key = 'f02034d0d7b24cb594f5c65f9fa525dd'
        consumer_secret = 'f5fac6873b544b5191809b5ee7f9b6fc'
        fs = Fatsecret(consumer_key, consumer_secret)
        result = fs.foods_search("Samosa")
        x = food.insert(result)
        print(result)
        return 'hello'
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
        # return 'hello'

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
        if x[0]['HEARTRATE'] == "" or x[0]['HEARTRATE'] == "NULL":
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
            print("DATABASE UPDATED ")
            return "DATABASE UPDATED "

        else:

            print("NOT REQUIRED! ALREADY FILLED")
            return 'NOT REQUIRED! ALREADY FILLED'


if __name__ == '__main__':
    app.run()
