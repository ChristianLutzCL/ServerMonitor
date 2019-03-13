from flask import Flask

from monitor import *

app = Flask(__name__)

@app.route("/")
def hello():
    return monitor_website("http://www.inspiredprogrammer.com/")