from flask import current_app
from flask_login import current_user
from monitor.models import ContiniousMonitoring, User
from monitor import db


def add_website(website_name='Test1234Monitor', website_url='https://monitor.inspiredprogrammer.com', isRunning=True, response_time='000', up_time='000'):
    uid = current_user.id
    website = ContiniousMonitoring(user_id=uid, website_name=website_name, website_url=website_url, isRunning=isRunning, response_time=response_time, up_time=up_time)
    db.session.add(website)
    db.session.commit()
    #run_monitoring()
    return website

def run_monitoring():
    websites = ContiniousMonitoring.query.filter_by(isRunning=True).all()
    

