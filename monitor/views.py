from flask import render_template, request
from monitor import app
from monitor.monitoring import monitor_website, ping, get_server_ip, check_latency, get_server_location
from monitor.models import CheckedWebsite, updateDatabase
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
