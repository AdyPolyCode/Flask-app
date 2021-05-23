from app import myApp, db
from flask import Flask, render_template, redirect, url_for, request, session, flash
from forms import RegisterForm, LoginForm
from models import User, Post
from flask_login import login_required, login_user, logout_user, current_user


@myApp.route('/home')
@myApp.route('/')
def home():
    return render_template('home.html', title='Home')


@myApp.route('/about')
def about():
    return render_template('about.html', title='About')



@myApp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Successfully logged in.')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccesful. Please check your login data.')
    return render_template('login.html', title='Login', form=form)


@myApp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data_collection = form.email.data, form.username.data, form.password.data
        user = User(username=data_collection[1], email=data_collection[0])
        user.hash_password(data_collection[2])
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@myApp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))