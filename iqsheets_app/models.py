import os
from datetime import datetime
from iqsheets_app import db, login_manager
from flask import redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

# Login Manager User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    job_description = db.Column(db.String(100), nullable=True)
    profile_picture = db.Column(db.String, nullable=True, default='default_profile_picture.png')
    password_hash = db.Column(db.String, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    premium = db.Column(db.Boolean, nullable=False, default=False)
    num_prompts = db.Column(db.Integer, nullable=False, default=0)
    num_tokens = db.Column(db.Integer, nullable=False, default=0)
    is_oauth = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    favorites = db.relationship('Favorite', backref="user")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        
    def __repr__(self):
        f"User with {self.id} and {self.username}, {self.email} was created."
class OAuth(OAuthConsumerMixin, db.Model):
    
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)
    
class Favorite(db.Model):
    
    __tablename__ = "favorites"
    
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    provider = db.Column(db.String, nullable=False)
    favorite_type = db.Column(db.String, nullable=False)
    method = db.Column(db.String, nullable=False)
    command = db.Column(db.String, nullable=False)
    prompt = db.Column(db.String, nullable=False)
    favorite_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def __init__(self, provider, favorite_type, method, command, prompt, user_id):
        self.provider = provider
        self.favorite_type = favorite_type
        self.method = method
        self.command = command
        self.prompt = prompt
        self.user_id = user_id
        
    def __repr__(self):
        f"Formel mit {self.provider}, {self.favorite_type}, {self.command}, {self.prompt} wurde am {self.favorite_date} hinzugefügt."

class Template(db.Model):
    
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(200), nullable=False, unique=True)
    template_category = db.Column(db.String(60), nullable=True)
    template_description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    bucket = db.Column(db.String(100))
    region = db.Column(db.String(100))
    s3_bucket_link = db.Column(db.String, nullable=False)
    
    def __init__(self, template_name, template_category, template_description, s3_bucket_link):
        self.template_name = template_name
        self.template_category = template_category
        self.template_description = template_description
        self.s3_bucket_link = s3_bucket_link
        
    def __repr__(self):
        f"Template {template_name}, wurde mit {template_category} am {created_at} hinzugefügt."
        