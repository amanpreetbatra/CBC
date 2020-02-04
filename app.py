from flask import Flask
from bson.objectid import ObjectId
from connection  import  *

app = Flask(__name__)


@app.route('/hello')
def hello_world():
    session =[]
    x = col.find({"_id": ObjectId("5e388991272e4c23e056d732")})
    print(x._id)
    return 'hello'
    # user = list(col.insert({"_id": session['_id'],"HEARTRATE":"NULL"}))
    #print(list(x))



if __name__ == '__main__':
    app.run()
