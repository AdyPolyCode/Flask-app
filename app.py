from flask import Flask, render_template, url_for

myApp = Flask(__name__)
myApp.config.update(
    DEBUG=True,
    SECRET_KEY='mysecretkey'

)

@myApp.route('/home')
@myApp.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    myApp.run()