from monitor import app
from monitor.monitoring import monitor_website
from flask import render_template, request


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        if request.form['url'] != '':
            url = request.form['url']
            response = monitor_website(url)
            return render_template('index.html', title="Home", response=response)
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
