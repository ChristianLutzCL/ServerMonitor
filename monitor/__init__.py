from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

#Flask and DB Keys
app.config['SECRET_KEY'] = environ.get('FLASK_SERVERMONITOR')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#API Keys
app.config['IPSTACK_API_KEY'] = environ.get('IPSTACK_KEY')

#app.config.from_envvar('APP_SETTINGS')
db = SQLAlchemy(app)

from monitor import views, forms

