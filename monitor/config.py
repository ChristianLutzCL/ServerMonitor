import os

class Config:

    #Flask and DB Keys
    SECRET_KEY = os.environ.get('FLASK_SERVERMONITOR')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

    #API Keys
    IPSTACK_API_KEY = os.environ.get('IPSTACK_KEY')

    #Private Email
    PRIVATE_MAIL = os.environ.get('EMAIL_PRIVATE')

    # Email config
    MAIL_SERVER = 'mail.inspiredprogrammer.com'
    MAIL_PORT = 465
    #MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')