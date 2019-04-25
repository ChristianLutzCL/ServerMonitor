from flask import render_template, request
from monitor import app
from monitor.monitoring import monitor_website, ping, get_server_ip, check_latency, get_server_location
from monitor.models import CheckedWebsite, updateDatabase
from sqlalchemy import desc


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
        return render_template('index.html', title="Is the website down? | ServerMonitor", url='url', status_code='status_code', status_reason='status_reason', lat='-', loc='-', ip='-', isdown='isdown', database_query=database_query)


@app.route("/info", methods=('GET', 'POST'))
def info():
    return render_template('info.html', title="Info | ServerMonitor")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
