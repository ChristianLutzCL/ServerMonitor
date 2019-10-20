from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from monitor import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class CheckedWebsite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    website_url = db.Column(db.String(80), unique=False, nullable=True)
    response_code = db.Column(db.String(10), unique=False, nullable=True)
    response_message = db.Column(db.String(10), unique=False, nullable=True)
    isdown = db.Column(db.Boolean)

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.check_date, self.website_url, self.response_code, self.response_message, self.isdown)


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True} 

    # Basic Account Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    account_creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password_reset_count = db.Column(db.Integer, nullable=False, default=0)
    last_password_reset = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, nullable=False, default=0)
    last_ip = db.Column(db.String, nullable=True)

    isStaff = db.Column(db.Boolean, nullable=False, default=False)
    isPayingUser = db.Column(db.Boolean, nullable=False, default=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', {self.email}', {self.image_file}')"


class ContiniousMonitoring(db.Model):
    __table_args__ = {'extend_existing': True} 

    # DB Metadata problem FIX
    # db.metadata.clear()

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer) #New Database - user_id = db.Column(db.Integer, db.ForeginKey('User.id'))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    website_name = db.Column(db.String(20), unique=False, nullable=False)
    website_url = db.Column(db.String(20), nullable=False)
    isRunning = db.Column(db.Boolean)
    response_time = db.Column(db.String, nullable=False)
    up_time = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.website_name, self.website_url, self.isRunning, self.response_time, self.up_time)


def updateDatabase(response):
    db.session.add(response)
    db.session.commit()




