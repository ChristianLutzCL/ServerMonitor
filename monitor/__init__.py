from flask import Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = '7d2e1a0f1b84b251f51ce34003689d8c'


import monitor.views
