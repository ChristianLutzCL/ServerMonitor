from flask import Blueprint

import os
from flask import render_template, request, flash, redirect, url_for, request
from monitor.monitoring import monitor_website, ping
from monitor.models import CheckedWebsite, updateDatabase
from sqlalchemy import desc

from monitor.main.utils import contact_mail

main = Blueprint('main', __name__, static_folder='static', static_url_path='/main/static') #static_folder='static', static_url_path='/main/static


@main.route("/", methods=['GET', 'POST'])
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


@main.route("/info", methods=('GET', 'POST'))
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


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




#=========================================
# Routes for PWA-Files
#=========================================

@main.route("/offline.html")
def offline():
    return main.send_static_file('offline.html')


@main.route("/service-worker.js")
def sw():
    return main.send_static_file('service-worker.js')


@main.route("/app.js")
def app():
    return main.send_static_file('app.js')


@main.route("/manifest.json")
def manifest():
    return main.send_static_file('manifest.json')



