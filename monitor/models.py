from monitor import db
from datetime import datetime


class CheckedWebsite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    website_url = db.Column(db.String(80), unique=False, nullable=True)
    response_code = db.Column(db.String(10), unique=False, nullable=True)
    response_message = db.Column(db.String(10), unique=False, nullable=True)
    isdown = db.Column(db.Boolean)

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.check_date, self.website_url, self.response_code, self.response_message, self.isdown)


def updateDatabase(response):
    db.session.add(response)
    db.session.commit()

