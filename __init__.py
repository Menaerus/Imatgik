from flask import Flask
import sys
sys.path.append('./lib')


from User import *
from Config import *
from Storage import *
from Authenticator import *

from flask_login import LoginManager
login_manager = LoginManager()


config = SimpleConfig("config.json")
storage = SimpleStorage(config)

@login_manager.user_loader
def load_user(user_id):
  authenticator = SimpleAuthenticator(config)

  return User.get(user_id, authenticator, storage)


def create_app():
  app = Flask(__name__)
  app.secret_key = b'1cbd0200c3d95d620cb4aecf00690e54dab36de6a2dea88987899a027db821bc'

  # blueprint for auth routes in our app
  from .Auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  # blueprint for some initial page of app
  from .Imatgik import imatgik as imatgik_blueprint
  app.register_blueprint(imatgik_blueprint)

  # blueprint for image management pages
  from .Images import img as images_blueprint
  app.register_blueprint(images_blueprint)

  login_manager.init_app(app)
  return app