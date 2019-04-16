from flask import render_template, request
from monitor import app
from monitor.monitoring import monitor_website, ping
from monitor.models import CheckedWebsite, updateDatabase
from sqlalchemy import desc


@app.route("/", methods=('GET', 'POST'))
def index():
    database_query = CheckedWebsite.query.order_by(desc(CheckedWebsite.check_date)).limit(10).all()

    if request.method == 'POST' and request.form['url'] != '':
        url = request.form['url']
        response = monitor_website(ping(url))
        database_return = CheckedWebsite(website_url=str(response[0]), response_code=str(response[1]), response_message=str(response[2]), isdown=response[3])
        updateDatabase(database_return)
        database_query_update = CheckedWebsite.query.order_by(desc(CheckedWebsite.check_date)).limit(10).all()
        return render_template('index.html', title="Home", response=response, database_query=database_query_update)
    else:
        return render_template('index.html', title="Home", response=monitor_website("https://www.google.com"), database_query=database_query)


@app.route("/info", methods=('GET', 'POST'))
def info():
    return render_template('info.html', title="Info")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
