from io import BytesIO
from flask import Flask, request, render_template, send_from_directory, Response, abort, session, redirect, url_for
from bson.objectid import ObjectId
from PIL import Image
from config import Config
from connection  import  *
import json
import views as v
import sys
import uuid
import os
from werkzeug.utils import secure_filename
import bcrypt
from authorise import *

#from forms import LoginForm



UPLOAD_FOLDER = "UPLOAD_FOLDER"
#login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object(Config)
#login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


@app.route('/')
def index():
    if 'username' in session:
        return render_template(url_for('crm'))

    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():

    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('crm'))

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass,'isadmin':'false'})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')





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



# @app.route('/login',methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for user {}, remember_me={}'.format(
#             form.username.data, form.remember_me.data))
#         return redirect('/crm')
#     return render_template('login.html', form=form)



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
    # print(inp)
    #
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
    app.run()
