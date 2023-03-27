"""Email functions with Flask-Mail"""
from flask import current_app as app
from flask_mail import Message
from formelwizzard_app import mail

def send_email(to, subject, template):
    """Function to send email

    Args:
        to (_type_): user
        subject (_str__): Registration/Password
        template (_type_): HTML Template
    """
    msg = Message(
        subject,
        recipients=[to],
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    msg.html = template
    mail.send(msg)
    