from flask_mail import Message

from excelguru_app import app, mail

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    msg.html = template
    mail.send(msg)
    