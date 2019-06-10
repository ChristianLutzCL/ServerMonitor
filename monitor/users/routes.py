from flask import Blueprint

import os
import secrets
from PIL import Image
from flask import render_template, request, flash, redirect, url_for, request
from monitor import db, bcrypt, mail
from monitor.monitoring import monitor_website, ping, get_server_ip, check_latency, get_server_location
from monitor.models import CheckedWebsite, updateDatabase, User
from monitor.users.forms import SignUpForm, SignInForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, AddWebsiteForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail  import Message
from sqlalchemy import desc

import time

from monitor.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/signup", methods=('GET', 'POST'))
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created! You are now able to login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('signup.html', title="Sign Up | ServerMonitor", form=form)


@users.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash(f'Login Unsuccessful! Please check email and password', 'danger')
    return render_template('login.html', title="Sign In | ServerMonitor", form=form)


@users.route("/logout", methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account", methods=('GET', 'POST'))
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('account.html', title="Your Account | ServerMonitor", image_file=image_file, form=form)


@users.route("/reset_password", methods=('GET', 'POST'))
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password | ServerMonitor", form=form)


@users.route("/reset_password/<token>", methods=('GET', 'POST'))
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password | ServerMonitor", form=form)


import random

@users.route("/monitoring", methods=('GET', 'POST'))
@login_required
def monitoring():
    form = AddWebsiteForm()

    if form.is_submitted:

        data = [] #Data for response time chart
        data2 = []

        for i in range(24):
            #time.sleep(0.1)
            data.append(check_latency('https://monitor.inspiredprogrammer.com'))
            #print(data)

        for i in range(24):
            data2.append(random.randint(200, 500))
        flash(data, 'success')
        #return redirect(url_for('users.login'))
        return render_template('monitoring.html', title="Monitor your websites2 | ServerMonitor", form=form, data_responsetime=data, data_uptime=data2)
    return render_template('monitoring.html', title="Monitor your websites | ServerMonitor", form=form)

