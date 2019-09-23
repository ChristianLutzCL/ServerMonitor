from flask import Blueprint

import os
import secrets
from PIL import Image
from flask import render_template, request, flash, redirect, url_for, request, jsonify
from monitor import db, bcrypt, mail
from monitor.monitoring import check_latency
from monitor.models import User, ContiniousMonitoring
from monitor.users.forms import SignUpForm, SignInForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, AddWebsiteForm, DeleteAccountForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail  import Message
from sqlalchemy import desc

import time
import json
from datetime import datetime

from monitor.users.utils import save_picture, send_reset_email, send_verification_email

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
            user.last_login = datetime.utcnow()
            user.login_count += 1
            user.last_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) #User IP or from server?
            db.session.commit()
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
    account_deletion_form = DeleteAccountForm()
    
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

    if account_deletion_form.validate_on_submit():
        if account_deletion_form.confirmation.data == current_user.email:
            user = User.query.filter_by(email=current_user.email).first()
            db.session.delete(user)
            logout_user()
            db.session.commit()
            flash('Your account has been successfully deleted. See you next time.', 'info')
        else:
            flash('Error', 'danger')
        return redirect(url_for('main.index'))

    return render_template('account.html', title="Your Account | ServerMonitor", image_file=image_file, form=form, deletion_form=account_deletion_form)


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
        user.last_password_reset = datetime.utcnow()
        user.password_reset_count += 1
        db.session.commit()
        flash(f'Your password has been updated! You are now able to login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password | ServerMonitor", form=form)


import random


@users.route("/websites", methods=('GET', 'POST'))
@login_required
def my_websites():
    form = AddWebsiteForm()
    return render_template('my_websites.html', title="My Websites | ServerMonitor", form=form)



#/monitoring only shows the graphs of the selected website
@users.route("/monitoring/<webiste_url>", methods=('GET', 'POST'))
@login_required
def monitoring(website_url):
    c = website_url
    form = AddWebsiteForm()

    data_responsetime = {
        "0000": 0,
        "0100": 0,
        "0200": 0,
        "0300": 0,
        "0400": 0,
        "0500": 0,
        "0600": 0,
        "0700": 0,
        "0800": 0,
        "0900": 0,
        "1000": 0,
        "1100": 0,
        "1200": 0,
        "1300": 0,
        "1400": 0,
        "1500": 0,
        "1600": 0,
        "1700": 0,
        "1800": 0,
        "1900": 0,
        "2000": 0,
        "2100": 0,
        "2200": 0,
        "2300": 0,
        "2400": 0
    }
    data_uptime = {
        "0000": 0,
        "0100": 0,
        "0200": 0,
        "0300": 0,
        "0400": 0,
        "0500": 0,
        "0600": 0,
        "0700": 0,
        "0800": 0,
        "0900": 0,
        "1000": 0,
        "1100": 0,
        "1200": 0,
        "1300": 0,
        "1400": 0,
        "1500": 0,
        "1600": 0,
        "1700": 0,
        "1800": 0,
        "1900": 0,
        "2000": 0,
        "2100": 0,
        "2200": 0,
        "2300": 0,
        "2400": 0
    }

    if form.validate_on_submit():
        current_hour = datetime.utcnow().hour
        current_hour_mil = str(current_hour) + '00'
        data_responsetime[current_hour_mil] = check_latency(form.website_url.data)
        
        response_time_json = json.dumps(data_responsetime)
        response_time_dict = json.loads(response_time_json)
        #data_responsetime.append(json.dumps({'current time': (check_latency(form.website_url.data))}))
        #t = json.dumps({'current time': (check_latency(form.website_url.data))})
        monitoring = ContiniousMonitoring(user_id=current_user.id, website_name=form.name.data, website_url=form.website_url.data, isRunning=form.monitoring_activated.data, response_time=response_time_json, up_time='leer')
        db.session.add(monitoring)
        db.session.commit()
        flash(f'\"{form.name.data}\" has been created!', 'success')
        
        return render_template('monitoring.html', title="Monitor your websites | ServerMonitor", form=form, website_url=form.website_url.data, monitoring_name=form.name.data, data_responsetime=list(response_time_dict.values()), data_uptime=data_responsetime)

    
    #mon = ContiniousMonitoring.query.filter_by(id=1).first()
    
    #print(mon.response_time)

    #s = json.loads(mon.response_time)
    #s['2400'] = check_latency(mon.website_url)
    #mon.response_time = json.dumps(s)

    #db.session.commit()
    #print(s.values())

    #v = json.loads(mon.response_time)

    return render_template('monitoring.html', title="Monitor your websites | ServerMonitor", form=form)#, website_url=mon.website_url, monitoring_name=mon.website_name, data_responsetime=list(v.values()))

