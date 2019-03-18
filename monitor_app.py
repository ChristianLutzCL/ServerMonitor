from flask import Flask, render_template, request

from monitor import monitor_website

app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        if request.form['url'] != '':
            url = request.form['url']
            response = monitor_website(url)
            return render_template('index.html', title="Home", response=response)
        else:
            return render_template('index.html', title="Home", response='ERROR')
    else:
        return render_template('index.html', title="Home")
