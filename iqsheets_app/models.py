''' IQ_Sheets DB Models '''
from datetime import datetime
import stripe
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from iqsheets_app import db, login_manager

# Login Manager User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    job_description = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now)
    cancellation_date = db.Column(db.DateTime, default=None, nullable=True)
    is_cancelled = db.Column(db.Boolean, default=False, nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    stripe_customer_id = db.Column(db.String, nullable=True, default=None)
    stripe_sub_id = db.Column(db.String, nullable=True, default=None)
    newsletter = db.relationship('Newsletter', backref='user')
    num_prompts = db.Column(db.Integer, nullable=False, default=0)
    num_tokens = db.Column(db.Integer, nullable=False, default=0)
    is_oauth = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    prompt = db.relationship('Prompt', backref="user")

    def check_password(self, password):
        """ check hashed password """ 
        return check_password_hash(self.password_hash, password)
     
    def check_payment(self):
        """ Check whether payment of a user was successful """
        # Stripe API Key
        if current_app.debug: 
            stripe.api_key = current_app.config['STRIPE_SECRETKEY_TEST']
        else:
            stripe.api_key = current_app.config['STRIPE_SECRETKEY_PROD']
        if self.is_admin is False:
            try:
                resp = stripe.Customer.list(email=self.email)
                if resp.get('data'):
                    print(resp["data"])
                    stripe_cust_id = resp["data"][0]["id"]
                    stripe_subscription_id = stripe.Subscription.list(customer=stripe_cust_id)
                    stripe_subscription_id = stripe_subscription_id["data"][0]["id"] 
                    self.stripe_customer_id = stripe_cust_id
                    self.stripe_sub_id = stripe_subscription_id
                    db.session.add(self)
                    db.session.commit()
                else:
                    self.stripe_customer_id = None
                    self.stripe_sub_id = None
                    db.session.add(self)
                    db.session.commit()
            except stripe.error.InvalidRequestError as e:
                # Handle the error, e.g., log it or raise a specific exception
                print(f"Error checking payment: {e}")
           
    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)
        
    def __repr__(self):
        f"User with {self.id} and {self.username}, {self.email} was created."

class OAuth(OAuthConsumerMixin, db.Model):
    
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    provider_user_email = db.Column(db.String(400), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

class Prompt(db.Model):
    """ DB Model for generated Prompts """ 
    
    __tablename__ = "prompts"
     
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    prompt_type = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    prompt = db.Column(db.String, nullable=False)
    result = db.Column(db.String)
    favorite = db.Column(db.Boolean, nullable=True, default=False)
    feedback = db.Column(db.Boolean, nullable=True)
    
    def __init__(self, prompt_type, category, prompt, result, user_id):
        self.prompt_type = prompt_type
        self.category = category
        self.prompt = prompt
        self.result = result
        self.user_id = user_id
        
    def __repr__(self):
        f"Formel mit {self.prompt_type}, {self.prompt} wurde am {self.created_at} hinzugefügt."

class Template(db.Model):
    """ Class for Excel Templates """  
    
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(200), nullable=False, unique=True)
    template_category = db.Column(db.String(60), nullable=True)
    template_description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    bucket = db.Column(db.String(100))
    region = db.Column(db.String(100))
    
    def __init__(self, template_name, template_category, template_description, folder, bucket, region):
        self.template_name = template_name
        self.template_category = template_category
        self.template_description = template_description
        self.folder = folder
        self.bucket = bucket
        self.region = region
        
    def __repr__(self):
        f"Template {template_name}, wurde mit {template_category} am {created_at} hinzugefügt."

class Newsletter(db.Model):
    """ DB Model for Newsletter registrations """ 
    
    __tablename__ = "newsletter"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    
    def __init__(self, email):
        self.email = email
        
    def __repr__(self):
        f"Newsletter mit {self.email} wurde am {self.created_at} hinzugefügt."
