from flask import render_template, request, flash, redirect, url_for, request
from monitor import app, db, bcrypt
from monitor.monitoring import monitor_website, ping, get_server_ip, check_latency, get_server_location
from monitor.models import CheckedWebsite, updateDatabase, User
from monitor.forms import SignUpForm, SignInForm
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc

import smtplib
import os

EMAIL_ADRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


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
        name = request.form['txtName']
        email = request.form['txtEmail']
        website = request.form['txtWebsite']
        message = request.form['txtMsg']
        mail(name, email, website, message)
        return render_template('info.html', title="SENT | ServerMonitor")
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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('account.html', title="Your Account | ServerMonitor", image_file=image_file)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



def mail(name, email, website, message):
    with smtplib.SMTP('smtp.googlemail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

        subject = 'InspiredProgrammer ServerMonitor - Contact Form'
        body = 'Mail from ' + name + ', ' + email + ' (' + website + ')\n\n' + message
        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(EMAIL_ADRESS, EMAIL_ADRESS, msg)
