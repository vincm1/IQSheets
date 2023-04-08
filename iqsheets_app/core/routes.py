''' Core routes for landing page etc. '''
from flask import Blueprint, current_app, render_template
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from .forms import NewsletterForm, ContactForm
from flask_mail import Message
from iqsheets_app import mail

def send_email(to, subject, body):
    """Function to send email

    Args:
        to (_type_): user
        subject (_str__): Registration/Password
        template (_type_): HTML Template
    """
    msg = Message(
        subject,
        recipients=[to],
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        body=body
    )
    print(msg)
    mail.send(msg)
    
################
#### config ####
################

core_blueprint = Blueprint('core', __name__)

def mailchimp_newsletter(email):
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": current_app.config['MAILCHIMP_API_KEY'],
            "server": current_app.config['MAILCHIMP_SERVERPREFIX']
        })

        response = client.lists.add_list_member(current_app.config['MAILCHIMP_AUDIENCE_ID'], {"email_address": email, "status": "subscribed"})
        print(response)
        return response
    
    except ApiClientError as error:
        print(error.status_code)
        return error.status_code
    
################
#### routes ####
################

@core_blueprint.route("/", methods=["GET","POST"])
@core_blueprint.route("/home", methods=["GET","POST"])
def index():
    form_nl = NewsletterForm()
    return render_template('index.html', form_nl=form_nl)

@core_blueprint.route("/impressum", methods=["GET"])
def impressum():
    form_nl = NewsletterForm()
    return render_template('impressum.html', form_nl=form_nl)

@core_blueprint.route("/kontakt", methods=["GET", "POST"])
def kontakt():
    form_nl = NewsletterForm()
    form_contact = ContactForm()
    if form_contact.validate_on_submit():
        send_email(
         to=current_app.config['KONTAKT_IQSHEETS'],
         subject=form_contact.betreff.data,
         body=form_contact.text.data + ', ' + form_contact.name.data + ', ' + form_contact.email.data
        )
    return render_template('kontakt.html', form_nl=form_nl, form_contact=form_contact)

@core_blueprint.route("/abos", methods=["GET", "POST"])
def pricing():
    form_nl = NewsletterForm()
    return render_template('pricing.html', form_nl=form_nl)

@core_blueprint.route("/newsletter", methods=["POST"])
def newsletter():
    form_nl = NewsletterForm()
    
    if form_nl.validate_on_submit():
        status = mailchimp_newsletter(form_nl.email.data)
  
    return render_template('index.html', form_nl=form_nl)
