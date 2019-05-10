import os


class Config:
    #Flask and DB Keys
    SECRET_KEY = os.environ.get('FLASK_SERVERMONITOR')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    #API Keys
    IPSTACK_API_KEY = os.environ.get('IPSTACK_KEY')

    # Email config
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')