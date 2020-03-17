from io import BytesIO
from flask import Flask, request, render_template, send_from_directory, Response,abort
from bson.objectid import ObjectId
from PIL import Image
from connection  import  *
import json
import views as v
import sys
import uuid
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "UPLOAD_FOLDER"


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Welcome to CBC</h1>"

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
    file = request.files['prod_img']
    if file.filename == '':
        print('No selected file')
    if file and v.allowed_file(file.filename):
        unique_filename = str(uuid.uuid4())
        ext = file.filename.rsplit('.', 1)[1].lower()
        file.filename = unique_filename +'.'+ext

        print(ext)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    data["prod_img"] = file.filename
    print(data)

    inp = v.custom_json(data)
    # print(inp)
    #
    return v.store_mealplan(inp)

@app.route('/delmealplan', methods= [ 'POST'])
def delmealplan():
    data = json.loads(request.data)
    x = list(v.get_mealplan(data["id"]))
    filename = secure_filename(x[0]['Prod_img'])
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    response = list(v.delete_mealplan(data["id"]))
    print(response)
    return 'ok'

@app.route('/updatemealplan', methods= [ 'POST'])
def updatemealplan():
    data = request.form.to_dict()
    if request.files['prod_img']:
        file = request.files['prod_img']
        if file and v.allowed_file(file.filename):
            unique_filename = str(uuid.uuid4())
            ext = file.filename.rsplit('.', 1)[1].lower()
            file.filename = unique_filename + '.' + ext
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data["prod_img"] = file.filename
            inp = v.custom_json(data)
            return v.update_mealplan(data['_id'], inp)
    else:
            x = list( v.get_mealplan(data['_id']))
            data['prod_img'] =x[0]["Prod_img"]
            inp = v.custom_json(data)
            return v.update_mealplan(data['_id'], inp)

@app.route('/<path:filename>')
def image(filename):
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    try:
        im = Image.open(filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = BytesIO()
        im.save(io, format='JPEG')
        return Response(io.getvalue(), mimetype='image/jpeg')

    except IOError:
        abort(404)

    return send_from_directory('.', filename)


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
