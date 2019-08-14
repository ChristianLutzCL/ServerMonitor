import os
from monitor import mail
from flask_mail  import Message

EMAIL_ADRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def contact_mail(name, email, website, message):
    msg = Message('InspiredProgrammer ServerMonitor - Contact Form', sender='noreply@inspiredprogrammer.com', recipients=['christian.lutz.privat@gmail.com'])
    msg.body = f'''
Mail from: {name},
Email: {email},
Website: ({website}),
--------------------------------------
Message:
{message}'''

    mail.send(msg)