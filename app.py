from logging import DEBUG
from flask import Flask

myApp = Flask(__name__)
myApp.config.update(
    DEBUG=True,
    SECRET_KEY=''
    
)

if __name__ == '__main__':
    myApp.run()