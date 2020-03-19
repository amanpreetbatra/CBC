from functools import wraps
from flask import abort, redirect, session, flash, url_for
from connection import users

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if 'username' in session:
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