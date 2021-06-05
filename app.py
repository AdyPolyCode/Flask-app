from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask_mail import Mail

myApp = Flask(__name__)
myApp.config['SECRET_KEY'] = '907fc501577a7dc638aca7592865aa18'
myApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
myApp.config['DEBUG'] = True
myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
myApp.config['REMEMBER_COOKIE_DURATION'] = timedelta(hours=1)
# myApp.permanent_session_lifetime = timedelta(seconds=10)
myApp.config['MAIL_SERVER']='smtp.mailtrap.io'
myApp.config['MAIL_PORT'] = 2525
myApp.config['MAIL_USERNAME'] = '70acc5813afd8c'
myApp.config['MAIL_PASSWORD'] = '1545207320cd98'
myApp.config['MAIL_USE_TLS'] = True
myApp.config['MAIL_USE_SSL'] = False
myApp.config['MAIL_DEFAULT_SENDER'] = 'noreply@some-company.com'

db = SQLAlchemy(myApp)
login_manager = LoginManager(myApp)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'You have to be logged in to access this page.'
login_manager.refresh_view = 'relog'
login_manager.needs_refresh_message_category = 'info'
login_manager.needs_refresh_message = 'Please log in again so you will be authorized to see this page.'

mail = Mail(myApp)



from routes import *

if __name__ == '__main__':
    myApp.run()