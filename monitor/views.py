import os
import secrets
from PIL import Image
from flask import render_template, request, flash, redirect, url_for, request
from monitor import app, db, bcrypt, mail
from monitor.monitoring import monitor_website, ping, get_server_ip, check_latency, get_server_location
from monitor.models import CheckedWebsite, updateDatabase, User
from monitor.forms import SignUpForm, SignInForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail  import Message
from sqlalchemy import desc

import smtplib
import os

EMAIL_ADRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


@app.route("/", methods=['GET', 'POST'])
def index():
    database_query = CheckedWebsite.query.order_by(desc(CheckedWebsite.check_date)).limit(10).all()

    if request.method == 'POST' and request.form['url'] != '':
        url = request.form['url']
        #response = monitor_website(ping(url))# respone = [0] r.url | [1] r.status_code | [2] r.reason | [3] server_ip | [4] latency | [5] server_location | [6] isdown
        url, status_code, status_reason, server_ip, server_latency, server_location, isdown = monitor_website(ping(url))
        database_return = CheckedWebsite(website_url=str(url), response_code=str(status_code), response_message=str(status_reason), isdown=isdown)
        updateDatabase(database_return)
        database_query_update = CheckedWebsite.query.order_by(desc(CheckedWebsite.check_date)).limit(10).all()
        return render_template('index.html', title="Is the website down? | ServerMonitor", url=url, status_code=status_code, status_reason=status_reason, ip=server_ip, lat=server_latency, loc=server_location, isdown=isdown, database_query=database_query_update)
    else:
        database_query_last = CheckedWebsite.query.order_by(desc(CheckedWebsite.check_date)).first() #CheckedWebsite.query.order_by(desc(CheckedWebsite.check_date)).limit(1).first()
        database_query_last_str = str(database_query_last)
        database_query_last_list = database_query_last_str.split()
        
        check_date = str(database_query_last_list[0] + " " + database_query_last_list[1])
        url = str(database_query_last_list[2])
        status_code = database_query_last_list[3]

        if status_code != 'NONE':
            status_code = int(database_query_last_list[3])
        else:
            status_code = 'NONE'

        status_reason = str(database_query_last_list[4])
        isdown = database_query_last_list[5]

        if isdown == 'True':
            isdown = True
        else:
            isdown = False

        return render_template('index.html', title="Is the website down? | ServerMonitor", url=url, status_code=status_code, status_reason=status_reason, lat='-', loc='-', ip='-', isdown=isdown, database_query=database_query)


@app.route("/info", methods=('GET', 'POST'))
def info():
    if request.method == 'POST':
        if request.form['txtName'] and request.form['txtEmail'] and request.form['txtMsg'] != '':
            name = request.form['txtName']
            email = request.form['txtEmail']
            website = request.form['txtWebsite']
            message = request.form['txtMsg']
            contact_mail(name, email, website, message)
            flash("Thank you for your message!" , 'success')
            return render_template('info.html', title="Message sent! | ServerMonitor")
        else:
            flash("Something went wrong. Please try again." , 'danger')
            return render_template('info.html', title="Info | ServerMonitor")
    else:
        return render_template('info.html', title="Info | ServerMonitor")


@app.route("/signup", methods=('GET', 'POST'))
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created! You are now able to login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title="Sign Up | ServerMonitor", form=form)


@app.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'Login Unsuccessful! Please check email and password', 'danger')
    return render_template('login.html', title="Sign In | ServerMonitor", form=form)


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_fn)
    
    output_sized = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_sized)
    i.save(picture_path)
    
    return picture_fn


@app.route("/account", methods=('GET', 'POST'))
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('account.html', title="Your Account | ServerMonitor", image_file=image_file, form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@inspiredprogrammer.com', recipients=[user.email])
    msg.body = f''' 
To reset your password, visit the following link: 
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)

@app.route("/reset_password", methods=('GET', 'POST'))
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title="Reset Password | ServerMonitor", form=form)


@app.route("/reset_password/<token>", methods=('GET', 'POST'))
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title="Reset Password | ServerMonitor", form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def contact_mail(name, email, website, message):
    with smtplib.SMTP('smtp.googlemail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

        subject = 'InspiredProgrammer ServerMonitor - Contact Form'
        body = 'Mail from ' + name + ', ' + email + ' (' + website + ')\n\n' + message
        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(EMAIL_ADRESS, EMAIL_ADRESS, msg)
