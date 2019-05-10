from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)

#Flask and DB Keys
app.config['SECRET_KEY'] = os.environ.get('FLASK_SERVERMONITOR')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#API Keys
app.config['IPSTACK_API_KEY'] = os.environ.get('IPSTACK_KEY')

#app.config.from_envvar('APP_SETTINGS')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Email config
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)

from monitor import views, forms

