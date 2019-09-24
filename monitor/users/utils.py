import os
import secrets
from PIL import Image
from flask import render_template, request, flash, redirect, url_for, request, current_app
from monitor import mail
from flask_mail  import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_fn)
    
    output_sized = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_sized)
    i.save(picture_path)
    
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@inspiredprogrammer.com', recipients=[user.email])
    msg.body = f''' 
To reset your password, visit the following link: 
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)


def send_verification_email(user):
    token = user.get_reset_token()
    msg = Message('Verificate your Email', sender='noreply@inspiredprogrammer.com', recipients=[user.email])
    msg.body = f'''
To verify your email adress, please visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)