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
    return render_template('index.html', title="Website monitoring that saves your time!")


@main.route("/blog", methods=('GET', 'POST'))
def blog():
        return render_template('blog.html', title="Blog | ServerMonitor")


@main.route("/thankyou", methods=('GET', 'POST'))
def thankyou():
    return render_template('thankyou.html', title="Thank You! | ServerMonitor")

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



