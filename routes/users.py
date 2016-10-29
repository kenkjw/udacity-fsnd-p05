from flask import Blueprint
from flask import flash
from flask import make_response
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import url_for
import json
from oauth2client import client
from oauth2client import crypt

from models import User
from utils import token
import config

Users_bp = Blueprint('users', __name__,template_folder='templates')


@Users_bp.route('/login')
def login():
    """Log the user out."""
    session['csrf'] = token()
    return render_template('login.html')


@Users_bp.route('/token', methods=['POST'])
def verify_token():
    token = request.form.get('token')
    csrftoken = request.form.get('csrftoken')
    provider = request.form.get('provider')

    if csrftoken != session['csrf']:
        response = make_response(json.dumps('Invalid CSRF token.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    session['csrf'] = ''
    try:
        token_info = client.verify_id_token(token, config.oauth['google']['client_id'])
        session['provider'] = 'google'
        session['name'] = token_info['name']
        session['email'] = token_info['email']
        user = User.by_email(token_info['email']) or User.create_user(session)
        session['user_id'] = user.id
        response = make_response(json.dumps('You have logged in.'),
                                     200)
        response.headers['Content-Type'] = 'application/json'
        return response        
    except crypt.AppIdentityError:
        response = make_response(json.dumps('Invalid token.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response



@Users_bp.route('/logout')
def logout():
    """Log the user out."""
    if 'provider' in session:
        del session['provider']
        del session['user_id']
        del session['name']
        del session['email']
    flash('You have successfully been logged out.')
    return redirect('/')