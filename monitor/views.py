from flask import render_template, request
from monitor import app
from monitor.monitoring import monitor_website
from monitor.models import CheckedWebsite, updateDatabase
from sqlalchemy import desc



@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST': #TODO: Rework whole response function
        if request.form['url'] != '':
            url = request.form['url']
            response = monitor_website(url)
            t = CheckedWebsite(website_url=str(response[0]), response_code=str(response[1]), response_message=str(response[2]))
            updateDatabase(t)
            o = CheckedWebsite.query.order_by(desc(CheckedWebsite.check_date)).limit(10).all()
            return render_template('index.html', title="Home", response=response, test=o)
        else:
            return render_template('index.html', title="Home", response=["ERROR", "ERROR", "ERROR"])
    else:
        return render_template('index.html', title="Home", response=monitor_website("https://www.google.de"))


@app.route("/info", methods=('GET', 'POST'))
def info():
    return render_template('info.html', title="Info")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
