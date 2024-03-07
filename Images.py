from flask import Blueprint, render_template, redirect, url_for, request, flash, session, make_response, send_file
from flask_login import login_required, current_user

from . import config
from . import storage


import sys
sys.path.append('./lib')
import os

def validfilename(filename):
  return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))

from Config import *


img = Blueprint('img', __name__) 

@img.route("/storage/<path:filename>")
@login_required
def serveimage(filename):
  if filename == 'No-Image-Placeholder.svg.png':
    return send_file('static/No-Image-Placeholder.svg.png')
  user = current_user
  response = storage.Send_File(user.get_id(), filename)
  if response != None:
    return response
  else:
    return render_template('notification.html', message='File not found (in our storage)', next=url_for("img.images"))

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
    image = user.images[session['index'] % len(user.images)]
    (_, simplefilename) = os.path.split(image)
    title = storage.GetTitle(user.get_id(), simplefilename)
  else:
    image = 'No-Image-Placeholder.svg.png'
    title = 'No Image, hence no title'
  return render_template("images.html", image=image, title=title)

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
  return render_template("confirmremove.html")

@img.route("/removeok", methods=["POST"])
@login_required
def removeok():
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
  title = request.form.get("title")
  if file != '':
    try:
      if validfilename(file.filename):
        if storage.GetTitle(current_user.get_id(), file.filename) != None:
          return render_template('notification.html', message='There is another image with same filename '+file.filename, next=url_for('img.upload'))
        storage.Store(current_user.get_id(), file, title)
      else:
        return render_template('notification.html', message='Invalid file type for an image', next=url_for("img.images"))
    except Exception:
      return render_template('notification.html', message='File not found', next=url_for("img.images"))
  return  redirect(url_for("img.images"))

@img.route("/edittitle", methods=["GET"])
@login_required
def edittitle():
  user = current_user
  if len(user.images) > 0:
    image = storage.CompleteName(user.get_id(), user.images[session['index'] % len(user.images)])
    (_, simplefilename) = os.path.split(image)
    title = storage.GetTitle(user.get_id(), simplefilename)
    return render_template("edittitle.html", title=title)
  return redirect(url_for("img.images"))

@img.route("/edittitleok", methods=["POST"])
@login_required
def edittitleok():
  title = request.form.get("title")
  user = current_user
  if len(user.images) > 0:
    filename = user.images[session['index'] % len(user.images)]
    (_, simplefilename) = os.path.split(filename)
    storage.StoreTitle(user.get_id(), simplefilename, title)
  return redirect(url_for("img.images"))


  