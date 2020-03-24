from functools import wraps
from flask import abort,jsonify, redirect, session, flash, url_for, request
from connection import users
import app


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if 'username' in session:
                u = users.find_one({'name': session['username']})
                if u["authorised"] == "true":
                    return f( *args, **kws)
            else:
                return redirect(url_for('index'))
    return decorated_function


def isadmin(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            u = users.find_one({'name': session['username']})
            if u["isadmin"] == 'true':
                return f( *args, **kws)
            else:
                flash("Only Admin Can Perform this action")
                abort(401)

    return decorated_function

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is Missing!'}),401

        try:
            if token == app.app.config["TOKEN"]:
                return f(*args, **kwargs)
            else:
                return jsonify({'message': 'Token is Invalid!'}), 401
        except:
            return jsonify({'message': 'Token is Invalid!'}),401

    return decorated