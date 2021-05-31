import os
from PIL import Image
from app import myApp, db
from flask import render_template, redirect, url_for, request, session, flash
from forms import RegisterForm, LoginForm, UpdateAccount, DeleteAccount, PostForm, EditPostForm
from models import User, Post
from flask_login import login_required, login_user, logout_user, current_user


@myApp.route('/home')
@myApp.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', title='Home', posts=posts)


@myApp.route('/about')
def about():
    return render_template('about.html', title='About')



@myApp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        data_collection = form.email.data, form.username.data, form.password.data, form.gender.data
        user = User(username=data_collection[1], email=data_collection[0], gender=data_collection[3])
        user.hash_password(data_collection[2])
        if form.gender.data == 'Male':
            user.profile_picture = 'man.png'
        if form.gender.data == 'Female':
            user.profile_picture = 'woman.png'
        db.session.add(user)
        db.session.commit()
        flash('Succesfully registered.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



def save_picture(form_pic):
    rnd_hex = os.urandom(8).hex()
    _, fHex = os.path.splitext(form_pic.filename)
    picFn = rnd_hex + fHex
    picPath = os.path.join(myApp.root_path, 'static/profile_pics', picFn)
    
    size = (125, 125)
    img = Image.open(form_pic)
    img.thumbnail(size)
    img.save(picPath)
    
    return picFn


@myApp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit() and current_user.check_password(form.password.data):
        if form.picture.data:
            pfile = save_picture(form.picture.data)
            current_user.profile_picture = pfile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated.')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    else:
        flash('Wrong password. Please try again.')
    image_file = url_for('static', filename='profile_pics/' + current_user.profile_picture)
    return render_template('account.html', title='Account', form=form, image_file=image_file)


@myApp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteAccount()
    if form.validate_on_submit():
        user = current_user
        if user.check_password(form.password.data):
            db.session.delete(user)
            db.session.commit()
            flash('Your account has been deleted.')
            return redirect(url_for('home'))
    return render_template('delete_account.html', title='Delete Account', form=form)


@myApp.route('/createPost', methods=['GET', 'POST'])
@login_required
def createPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, text=form.content.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post succesfully created!')
        return redirect(url_for('home'))
    return render_template('post.html', title='New Post', form=form)


@myApp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@myApp.route('/post/<int:user_id>')
def user_post(user_id):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=user_id).first_or_404()
    posts = Post.query.filter_by(user=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user_post.html', title=f'Posts by {user.username}', user=user, posts=posts)


@myApp.route('/post/my_posts')
@login_required
def ownedPost():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(user=current_user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('myposts.html', title='My Posts', posts=posts)


@myApp.route('/post/my_posts/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editPost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form = EditPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.content.data
        db.session.commit()
        flash('Post has been updated!')
        return redirect(url_for('ownedPost'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.text
    return render_template('editpost.html', title='Edit Post', form=form)