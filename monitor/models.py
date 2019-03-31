from monitor import db


class CheckedWebsite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #check_date = db.Column(db.DateTime)
    website_url = db.Column(db.String(80), unique=False, nullable=True)
    response_code = db.Column(db.String(10), unique=False, nullable=True)
    response_message = db.Column(db.String(10), unique=False, nullable=True)
    #isOnline = db.Column(db.Boolean)

    def __repr__(self):
        return self.website_url

