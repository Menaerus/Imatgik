from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user

from . import config
from . import storage
import sys
sys.path.append('./lib')
import os

img = Blueprint('img', __name__)

@img.route("/images")
@login_required
def images():
  user = current_user
  user.Fill(storage)
  try:
    index = session['index']
  except KeyError:
    session['index'] = 0
  if len(user.images) > 0:
    image = storage.CompleteName(user.get_id(), user.images[session['index'] % len(user.images)])
  else:
    image = 'No-Image-Placeholder.svg.png'
  return render_template("images.html", image=image)

@img.route("/prev")
@login_required
def prev():
  session['index'] -= 1
  return redirect(url_for("img.images"))

@img.route("/next")
@login_required
def next():
  session['index'] += 1
  return redirect(url_for("img.images"))

@img.route("/remove")
@login_required
def remove():
  user = current_user
  if len(user.images) > 0:
    filename = user.images[session['index'] % len(user.images)]
    storage.Remove(user.get_id(), filename)
  return redirect(url_for("img.images"))


@img.route("/upload", methods=['GET'])
@login_required
def upload():
  return render_template("upload.html")

@img.route("/uploadok", methods=['POST'])
@login_required
def uploadok():
  file = request.files['file']
  if file != '':
    storage.Store(current_user.get_id(), file)
  return  redirect(url_for("img.images"))
