import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


app.config['SECRET_KEY']="Kkr@6362"

#####################################################################
                    #DATABASE SETUP

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(BASE_DIR,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

db=SQLAlchemy(app)
Migrate(app,db)

#####################################################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

from project.core.views import core
from project.users.views import users

app.register_blueprint(core)
app.register_blueprint(users)
