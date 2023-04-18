''' Core routes for landing page etc. '''
from flask import Blueprint, current_app, render_template
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from flask_mail import Message
from iqsheets_app import mail
from .forms import NewsletterForm, ContactForm

################
#### config ####
################

core_blueprint = Blueprint('core', __name__)

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

def mailchimp_newsletter(email):
    ''' register user to mailchimp newsletter audience '''
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

@core_blueprint.route("/home", methods=["GET","POST"])
@core_blueprint.route("/start", methods=["GET","POST"])
@core_blueprint.route("/", methods=["GET","POST"])
def index():
    ''' Landing Page '''
    form_nl = NewsletterForm()
    return render_template('index.html', form_nl=form_nl)

@core_blueprint.route("/impressum", methods=["GET"])
def impressum():
    ''' Imprint page '''
    form_nl = NewsletterForm()
    return render_template('impressum.html', form_nl=form_nl)

@core_blueprint.route("/feedback", methods=["GET", "POST"])
@core_blueprint.route("/kontakt", methods=["GET", "POST"])
def kontakt():
    ''' Contact Page '''
    form_nl = NewsletterForm()
    form_contact = ContactForm()
    if form_contact.validate_on_submit():
        send_email(
            to=current_app.config['KONTAKT_IQSHEETS'],
            subject=form_contact.betreff.data,
            body=form_contact.text.data + ', ' + form_contact.name.data + ', ' 
                + form_contact.email.data)
    return render_template('kontakt.html', form_nl=form_nl, form_contact=form_contact)

@core_blueprint.route("/abos", methods=["GET", "POST"])
def pricing():
    ''' Abos and Pricing Page '''
    form_nl = NewsletterForm()
    return render_template('pricing.html', form_nl=form_nl)

@core_blueprint.route("/newsletter", methods=["POST"])
def newsletter():
    ''' Newsletter subscription route ''' 
    form_nl = NewsletterForm()   
    if form_nl.validate_on_submit():
        mailchimp_newsletter(form_nl.email.data)
    return render_template('index.html', form_nl=form_nl)
