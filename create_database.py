#Setup and create database file

from monitor.models import CheckedWebsite, User

from monitor import db, create_app
db.create_all(app=create_app())

app = create_app()
app.app_context().push()

with app.app_context():
    # Create CheckedWebsite
    new_website = CheckedWebsite(website_url='https://monitor.inspiredprogrammer.com', response_code='200', response_message='OK', isdown=False)
    db.session.add(new_website)
    db.session.commit()

    # Create User
    new_user = User(username='TestUser', email='test@test.com', password='123456')
    db.session.add(new_user)
    db.session.commit()