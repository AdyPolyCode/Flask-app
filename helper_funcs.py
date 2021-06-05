import os
from PIL import Image
from app import myApp, mail
from flask_mail import Message
from flask import url_for


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


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message(recipients=['0a57a1b068-03ff75@inbox.mailtrap.io'])
    message.subject = f'Password reset token - reset token for {user.username}'
    message.body = f'''
    Warning! Please dont answer to this message, if so noone will reply to you.

    To reset your password visit the following link: {url_for('reset_password', token=token, _external=True)}

    This email was send because of password reset. The link is provided below, The token will not be available after 30 minutes.
    '''
    mail.send(message)