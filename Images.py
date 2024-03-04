from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from . import config
from . import storage
import sys
sys.path.append('./lib')

img = Blueprint('img', __name__)


@img.route("/images")
@login_required
def images():
  user = current_user
  user.Fill(storage)
  print("User images = ", user.images)
  if len(user.images) > 0:
    image = user.images[user.current_image_index]
  else:
    image = ''
  return render_template("images.html", image=image)

@img.route("/prev")
@login_required
def prev():
  return render_template("images.html")

@img.route("/next")
@login_required
def next():
  return render_template("images.html")

@img.route("/remove")
@login_required
def remove():
  return render_template("images.html")

@img.route("/upload", methods=['GET'])
@login_required
def upload():
  return render_template("upload.html")

@img.route("/uploadok", methods=['POST'])
@login_required
def uploadok():
  file = request.files['file']
  storage.Store(current_user.get_id(), file)
  return render_template("images.html")
