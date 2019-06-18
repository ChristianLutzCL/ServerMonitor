from flask import current_app
from monitor.models import ContiniousMonitoring
from apscheduler.schedulers.background import BackgroundScheduler

import os
import time
import atexit


def add_monitoring():
    pass


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


def initial_scheduler():
    ''' Checks the time until full hour is reached '''
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger='interval', seconds=1)
    scheduler.start()

def hourly_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger='interval', seconds=3600)
    scheduler.start()


atexit.register(lambda: scheduler.shutdown())