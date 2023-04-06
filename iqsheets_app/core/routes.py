''' Core routes for landing page etc. '''
from flask import Blueprint, current_app, render_template
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from .forms import NewsletterForm, BetaTestForm

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
    form_bt = BetaTestForm()
    return render_template('index.html', form_nl=form_nl, form_bt=form_bt)

@core_blueprint.route("/abos")
def pricing():
    return render_template('pricing.html')

@core_blueprint.route("/newsletter", methods=["POST"])
def newsletter():
    form_nl = NewsletterForm()
    
    if form_nl.validate_on_submit():
        print(form_nl.email.data)
        status = mailchimp_newsletter(form_nl.email.data)
  
    return render_template('index.html', form_nl=form_nl)

@core_blueprint.route("/beta")
def beta():
    form_nl = NewsletterForm()
    form_bt = BetaTestForm()
    
    form = NewsletterForm()
    status = mailchimp_newsletter(form.email.data)
         
    return render_template('index.html', form_nl=form_nl, form_bt=form_bt)