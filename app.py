from io import BytesIO
from flask import Flask, render_template, send_from_directory, Response
from PIL import Image
from config import Config
import json
import views as v
import sys
import uuid
import os
from werkzeug.utils import secure_filename
from authorise import *


app = Flask(__name__)
app.config.from_object(Config)


''' THIS IS THE SEARCH API WHICH TAKES TWO INPUTS 1. Search String 2. Page Number'''


@app.route('/foodsearch', methods= ['POST'])
@token_required
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
@token_required
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
@token_required
def fetch_heart():
    data = json.loads(request.data)
    return v.fetch_heartrate(data)


@app.route('/customfoodins', methods= ['POST'])
@token_required
def custom_meal():
    data = json.loads(request.data)
    return v.store_mealplan(data)


@app.route('/inp_insight', methods= ['POST'])
@token_required
def insights():
    data = json.loads(request.data)
    return v.store_insights(data)



@app.route('/in_hr', methods= [ 'POST'])
@token_required
def insert_hr():
    if request.method == 'POST':
        data = json.loads(request.data)
        return v.insert_hr(data)

@app.route('/insert_weight', methods= [ 'POST'])
@token_required
def insert_weight():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            return v.insert_weight(data)
        except:
            e = sys.exc_info()[0:2]
            dat = {"message": str(e)}

            return json.dumps(dat),403

@app.route('/ret_weight', methods=["POST"])
def ret_weight():
    data = json.loads(request.data)
    return v.return_weight(data)

''' FOR ADDING IMAGES IN NUTRITION COLLECTION'''


@app.route('/image_nutri', methods= [ 'GET'])
@authorize
def addimages():
    data = list(v.show_nutrition())
    return render_template("addimages.html", data=data)

@app.route('/getnutriplan', methods= [ 'POST'])
@authorize
def getnutriplan():
    data = json.loads(request.data)

    response = list(v.get_nutrition(data["id"]))
    response[0]["_id"] = str(response[0]["_id"])

    response = json.dumps(response)
    return response

@app.route('/updatenutritionplan', methods= [ 'POST'])
@authorize
def updatenutriplan():
    data = request.form.to_dict()
    data = json.loads(data["data"])[0]
    if request.files['prod_img']:
        file = request.files['prod_img']
        if file and v.allowed_file(file.filename):
            unique_filename = str(uuid.uuid4())
            ext = file.filename.rsplit('.', 1)[1].lower()
            file.filename = unique_filename + '.' + ext
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data["prod_img"] = file.filename
            return v.update_nutriplan(data['_id'], data)
    else:
            x = list( v.get_nutrition(data['_id']))
            if "prod_img" in x[0]:
                data['prod_img'] =x[0]["prod_img"]
            else:
                data['prod_img'] = ""
                print(data)
            return v.update_nutriplan(data['_id'], data)


@app.route('/delnutriplan', methods= [ 'POST'])
@authorize
@isadmin
def delnutriplan():
    data = json.loads(request.data)
    x = list(v.get_nutrition(data["id"]))
    filename = secure_filename(x[0]['prod_img'])
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    response = list(v.delete_nutriplan(data["id"]))
    print(response)
    return 'ok'



''' ALL THE ENDPOINTS BELOW THIS POINT ARE FOR CRM OF STORING CUSTOM FOOD DATA N THE DATABASE'''


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('crm',_external=True))
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    return v.login()



@app.route('/logout')
def logout():
   x = v.logout()
   return x


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form
        return v.register(data)
    return render_template('register.html')


@app.route('/crm', methods= [ 'GET'])
@authorize
def crm():
    data = list(v.show_mealplan())
    return render_template("crm.html", data=data)

@app.route('/getmealplan', methods= [ 'POST'])
@authorize
def crm_1():
    data = json.loads(request.data)

    response = list(v.get_mealplan(data["id"]))
    response[0]["_id"] = str(response[0]["_id"])

    response = json.dumps(response)
    return response


@app.route('/storemealplan', methods= [ 'POST'])
@authorize
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
    return v.store_mealplan(inp)

@app.route('/delmealplan', methods= [ 'POST'])
@authorize
@isadmin
def delmealplan():
    data = json.loads(request.data)
    x = list(v.get_mealplan(data["id"]))
    filename = secure_filename(x[0]['Prod_img'])
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    response = list(v.delete_mealplan(data["id"]))
    print(response)
    return 'ok'

@app.route('/updatemealplan', methods= [ 'POST'])
@authorize
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
@authorize
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

