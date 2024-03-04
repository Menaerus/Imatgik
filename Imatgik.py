from flask import Flask, render_template, Blueprint

imatgik = Blueprint('imatgik', __name__)



@imatgik.route('/')
def index():
    return render_template('welcome.html')

@imatgik.route('/images')
def images():
    return render_template('images.html')


