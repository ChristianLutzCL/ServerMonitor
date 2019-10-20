from flask import Blueprint

import os
from flask import render_template, request, flash, redirect, url_for, request, jsonify
from flask_login import login_required
from monitor.models import User, ContiniousMonitoring
from monitor.users import continious_monitoring
from monitor import db



api = Blueprint('api', __name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]


@api.route("/api/v1/user/<int:user_id>", methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    return jsonify({'last login': user.last_login, 'registration date': user.account_creation_date, 'user_id': user.id ,'name': user.username, 'email': user.email})


@api.route("/api/v1/monitoring", methods=['GET'])
@login_required
def get_monitoring():
    monitoring = ContiniousMonitoring.query.filter_by(id=1).first()

    return jsonify({'website_name': monitoring.website_name, 'website_url': monitoring.website_url, 'isRunning': monitoring.isRunning, 'repsonse_time': monitoring.response_time})



@api.route("/api/v1/add_website", methods=['GET'])
@login_required
def add_website():
    website_name = request.args.get('website_name', default='ServerMonitor', type=str)
    website_url = request.args.get('website_url', default='https://monitor.inspiredprogrammer.com', type=str)
    continious_monitoring.add_website(website_name, website_url)
    return jsonify('Website', {'Website name': website_name, 'Website URL': website_url})