from app import myApp, db
from flask import render_template, redirect, url_for, request, session, flash
from forms import RegisterForm, LoginForm, UpdateAccount, DeleteAccount, PostForm, EditPostForm, SendResetTokenForm, ResetPasswordForm
from models import User, Post, Emoji, collection
from flask_login import login_required, login_user, logout_user, current_user, fresh_login_required
from helper_funcs import save_picture, send_reset_email


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
    session.permanent = True
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_p = request.args.get('next')
            flash('Successfully logged in.', category='success')
            if next_p:
                return redirect(next_p)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login unsuccesful. Please check your login data.', category='danger')
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
        user.coins = 10
        if form.gender.data == 'Male':
            user.profile_picture = 'man.png'
        if form.gender.data == 'Female':
            user.profile_picture = 'woman.png'
        db.session.add(user)
        db.session.commit()
        flash('Succesfully registered.', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@myApp.route('/account', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def account():
    user_emojis = current_user.emojis
    form = UpdateAccount()
    if form.validate_on_submit() and current_user.check_password(form.password.data):
        if form.picture.data:
            pfile = save_picture(form.picture.data)
            current_user.profile_picture = pfile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated.', category='info')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    else:
        flash('Wrong password. Please try again.', category='warning')
    image_file = url_for('static', filename='profile_pics/' + current_user.profile_picture)
    return render_template('account.html', title='Account', form=form, image_file=image_file, user_emojis=user_emojis)


@myApp.route('/delete', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def delete_account():
    form = DeleteAccount()
    if form.validate_on_submit():
        user = current_user
        if user.check_password(form.password.data):
            db.session.delete(user)
            db.session.commit()
            flash('Your account has been succesfully deleted.', category='info')
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
        flash('Post has been created!', category='info')
        return redirect(url_for('home'))
    return render_template('post.html', title='New Post', form=form)


@myApp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@myApp.route('/relog')
def relog():
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
        flash('Post has been updated!', category='info')
        return redirect(url_for('ownedPost'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.text
    return render_template('editpost.html', title='Edit Post', form=form)


@myApp.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash(f'Post {post.title} has been deleted.', 'info')
    return redirect(url_for('home'))


@myApp.route('/store')
@login_required
def smile_store():
    emojis = Emoji.query.all()
    return render_template('smile_store.html', title='Store', emojis=emojis)


@myApp.route('/coin_store')
@login_required
def coin_store():
    return render_template('coin_store.html', title='Coin Store')


@myApp.route('/coin_store/coin/<int:id>')
@login_required
def buy_coin(id):
    current_user.coins += id
    db.session.commit()
    flash(f'Item w successfully bought for w$!', 'success')
    return redirect(url_for('coin_store'))


@myApp.route('/emoji/<int:id>')
@login_required
def buy_emoji(id):
    emoji = Emoji.query.filter_by(id=id).first()
    user_emojis = current_user.emojis
    if emoji not in user_emojis:
        if emoji.price <= current_user.coins:
            current_user.emojis.append(emoji)
            db.session.commit()
            flash(f'Item {emoji.name} successfully bought.', 'success')
            return redirect(url_for('smile_store'))
        else:
            flash('You dont have enough coins to buy this item!', 'danger')
            return redirect(url_for('smile_store'))
    else:
        flash('You already have this item!', 'warning')
        return redirect(url_for('smile_store'))


@myApp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or expired reset token', 'warning')
        return redirect(url_for('send_reset_token'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.hash_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been recovered.', 'info')
        return redirect(url_for('login'))

    return render_template('reset_password.html', title='Reset Password', form=form)


@myApp.route('/send_reset_token', methods=['GET', 'POST'])
def send_reset_token():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SendResetTokenForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'Reset token has been sent to {user.email}', 'info')
        return redirect(url_for('home'))

    return render_template('send_reset_token.html', title='Forgot Account', form=form)