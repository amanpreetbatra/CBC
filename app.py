from flask import Flask, request
from bson.objectid import ObjectId
from connection  import  *
import json
from views import  food_search


app = Flask(__name__)

@app.route('/search', methods= ['POST'])
def food_s():
    x = json.loads(request.data)

    return food_search(x['data'])
    #else:
     #   return 'This method is not acceptable'

@app.route('/hello', methods= ['GET', 'POST'])
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
