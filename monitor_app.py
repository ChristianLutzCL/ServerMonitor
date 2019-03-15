from flask import Flask, render_template, request

from monitor import *

app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        if request.form['url'] != '':
            url = request.form['url']
            return render_template('index.html', title="Home", a=monitor_website('https://' + url))
            #return monitor_website("http://www.inspiredprogrammer.com/")
        else:
            return render_template('index.html', title="Home", a=monitor_website('https://www.google.de'))
    else:
        url = 'google.de'
        return render_template('index.html', title="Home", a=monitor_website('https://' + url))

