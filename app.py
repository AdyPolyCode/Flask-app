from flask import Flask, render_template, redirect, url_for, request, session
from forms import RegisterForm, LoginForm

myApp = Flask(__name__)
myApp.config.update(
    DEBUG=True,
    SECRET_KEY='674bcaca65cfc8ade8f5af8c4a23dedd'

)

potatoDatabase = {
    'admin': {
        'email': 'admin@dot.com',
        'password': 'admin123456789',
        'username': 'admin'},
    'test': {
        'email': 'test@dot.com',
        'password': 'test123456789',
        'username': 'test'
    }
}



@myApp.route('/home')
@myApp.route('/')
def home():
    user = session.get('username')
    return render_template('home.html', title='Home', user=user)


@myApp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = (request.form['email'], request.form['password'])
        real = True if u[0] in [list(data.values())[0] for data in potatoDatabase.values()] else None
        if real:
            for value in potatoDatabase.values():
                if value['email'] == u[0]:
                    if value['password'] == u[1]:
                        session['username'] = value['username']
                        return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)


@myApp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        info = request.form['email'], request.form['username'],\
            request.form['password']
        potatoDatabase[info[1]] = {
            'email': info[0],
            'password': info[2],
            'username': info[1]
        }
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@myApp.route('/logout')
def logout():
    user = session.get('username')
    if user:
        session.pop('username', None)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    myApp.run()