"""Email functions with Flask-Mail"""
from datetime import datetime, timedelta
from flask import current_app as app
from flask_mail import Message
from iqsheets_app import db
from iqsheets_app.models import User
from iqsheets_app import mail
from ..extensions import scheduler
from .token import generate_confirmation_token, confirm_token

def send_email(to, subject, message):
    """Function to send email

    Args:
        to (_type_): user
        subject (_str__): Registration/Password
        template (_type_): HTML Template
    """
    msg = Message(
        subject,
        body=message,
        recipients=[to],
        sender=app.config['MAIL_DEFAULT_SENDER']
        )
    mail.send(msg)

def send_reminder_unconfirmed_email():
    """ Automated email job sending to unconfirmed users """
    with scheduler.app.app_context():
        # Get the current date and time
        current_date = datetime.now()
        # Query all users that are not confirmed
        users = User.query.filter_by(is_confirmed=False).all()       
        for user in users:
            print(user)
            if user.registration_date < current_date - timedelta(days=1):
                token = generate_confirmation_token(user.email)
                confirm_url = confirm_url = f"https://www.iqsheets.de/confirm_email?token={token}"
                message = 'Bitte bestätige noch Deinen Account. Das ist dein Bestätigungslink: ' + confirm_url
                subject = "Email bestätigen für IQSheets!"
                send_email(user.email, subject, message)

def send_reminder_abo_email():
    """ Automated email job sending to users not subscribing """
    with scheduler.app.app_context():
        # Get the current date and time
        current_date = datetime.now()
        # Query all users that are not confirmed
        users = User.query.filter_by(sub_created=None).all()     
        for user in users:
            print(user)
            if user.registration_date < current_date - timedelta(days=1):
                if app.debug:
                    stripe_user_payment_link = app.config["STRIPE_TEST_PAYMENTPAGE"]
                else:
                    stripe_user_payment_link = app.config["STRIPE_PROD_PAYMENTPAGE"]
                message = f"Schließe jetzt dein IQSheets Premium Abo ab. Hier kannst Du ein Abo abschließen: {stripe_user_payment_link}"
                subject = "Starte jetzt dein IQSheets Abo!"
                send_email(user.email, subject, message)
            