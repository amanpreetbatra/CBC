from flask import Flask
from bson.objectid import ObjectId
from connection  import  *
import json

app = Flask(__name__)


@app.route('/hello')
def hello_world():
    x = list(col.find({"_id": ObjectId("5e388991272e4c23e056d732")}))
    oid = x[0]['_id']
    user = col.update({"_id": ObjectId(oid)},{

    "EXERCISE" : "PUSHUP",
    "GENDER" : "MALE",
    "LEVEL" : "BEGINNER",
    "REPS" : "LOW",
    "AGE" : "A",
    "lift WEIGHT" : "HEAVY",
    "HEARTRATE" : "NULL",
    "PID" : "1"
                })
    print(user)
    return 'hello'



if __name__ == '__main__':
    app.run()
