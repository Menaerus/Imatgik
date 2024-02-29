from flask import Flask
from flask import render_template

import sys
sys.path.append('./lib')

from Config import *
from Storage import *
from Authenticator import *

config = SimpleConfig("config.json")
storage = SimpleStorage(config)
authenticator = SimpleAuthenticator(config)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("welcome.html")


