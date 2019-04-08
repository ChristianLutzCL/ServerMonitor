from flask import render_template, request
from monitor import app
from monitor.monitoring import monitor_website, get_server_ip
from monitor.models import CheckedWebsite, updateDatabase
from sqlalchemy import desc


@app.route("/", methods=('GET', 'POST')) #TODO: Rework whole response method
def index():
    database_query = CheckedWebsite.query.order_by(desc(CheckedWebsite.check_date)).limit(10).all()
    if request.method == 'POST':
        if request.form['url'] != '':
            url = request.form['url']
            response = monitor_website(url)
            t = get_server_ip('inspiredprogrammer.com')
            print(t)
            database_return = CheckedWebsite(website_url=str(response[0]), response_code=str(response[1]), response_message=str(response[2]))
            updateDatabase(database_return)
            database_query = CheckedWebsite.query.order_by(desc(CheckedWebsite.check_date)).limit(10).all()

            return render_template('index.html', title="Home", response=response, database_query=database_query)
        else:
            return render_template('index.html', title="Home", response=["ERROR", "ERROR", "ERROR"], database_query=database_query)
    else:
        return render_template('index.html', title="Home", response=monitor_website("https://www.google.de"), database_query=database_query)


@app.route("/info", methods=('GET', 'POST'))
def info():
    return render_template('info.html', title="Info")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
