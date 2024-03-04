from flask import Blueprint, render_template, redirect, url_for, request, session
from . import login_manager
from . import config
from . import storage
from flask_login import login_user, logout_user

import sys
sys.path.append('./lib')

from User import *
from Factory import *

auth = Blueprint('auth', __name__)
img = Blueprint('img', __name__)

@auth.route('/login')
def login():
  return render_template('login.html')

@auth.route("/login", methods=['POST'])
def login_post():
  username = request.form.get('username')
  password = request.form.get('password')
  myauthenticator = MakeAuthenticator(config)
  if myauthenticator.Registered(username):
    if myauthenticator.Authenticate(username, password):
      user = User(username, password)
      user.is_authenticated = True
      user.is_active = True
      user.Fill(storage)
      login_user(user, remember=request.form.get('remember'))
      session['index'] = 0
      return redirect(url_for('img.images'))
  else:
    return redirect(url_for('auth.register'))
  return redirect(url_for('auth.login'))


@auth.route('/register')
def register():
  return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
  username = request.form.get('username')
  password = request.form.get('password')
  myauthenticator = MakeAuthenticator(config)
  if myauthenticator.Register(username, password):
    return redirect(url_for('auth.login'))
  return redirect(url_for('auth.alreadyregistered'))

@auth.route('/alreadyregistered')
def alreadyregistered():
  return render_template('alreadyregistered.html')

@auth.route('/logout')
def logout():
  logout_user()
  return redirect(url_for("auth.login"))

