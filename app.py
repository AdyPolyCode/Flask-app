from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta

myApp = Flask(__name__)
myApp.config['SECRET_KEY'] = '907fc501577a7dc638aca7592865aa18'
myApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
myApp.config['DEBUG'] = True
myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
myApp.config['REMEMBER_COOKIE_DURATION'] = timedelta(hours=1)

db = SQLAlchemy(myApp)
login_manager = LoginManager(myApp)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'You have to be logged in to access this page.'

from routes import *

if __name__ == '__main__':
    myApp.run()