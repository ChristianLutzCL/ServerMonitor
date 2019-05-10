import os
import secrets
from PIL import Image
from flask import render_template, request, flash, redirect, url_for, request, current_app
from monitor import  db, bcrypt, mail
from monitor.monitoring import monitor_website, ping, get_server_ip, check_latency, get_server_location
from monitor.models import CheckedWebsite, updateDatabase, User
from monitor.users.forms import SignUpForm, SignInForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail  import Message
from sqlalchemy import desc

import smtplib

EMAIL_ADRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def contact_mail(name, email, website, message):
    with smtplib.SMTP('smtp.googlemail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

        subject = 'InspiredProgrammer ServerMonitor - Contact Form'
        body = 'Mail from ' + name + ', ' + email + ' (' + website + ')\n\n' + message
        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(EMAIL_ADRESS, EMAIL_ADRESS, msg)