from datetime import datetime
from excelguru_app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    premium = db.Column(db.Boolean, nullable=False, default=False)
    favorites = db.relationship('Favorite', backref="user")
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, email, password, is_confirmed=False, confirmed_on=None):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.is_confirmed = is_confirmed
        self.confirmed_on = confirmed_on
        
    def __repr__(self):
        f"User with {self.id} and {self.username} {self.email}."
class OAuth(OAuthConsumerMixin, db.Model):
    
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

class Favorite(db.Model):
    
    __tablename__ = "favorites"
    
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    favorite_method = db.Column(db.String, nullable=False)
    favorite_type = db.Column(db.String, nullable=False)
    command = db.Column(db.String, nullable=False)
    prompt = db.Column(db.String, nullable=False)
    favorite_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def __init__(self, favorite_method, favorite_type, command, prompt, user_id):
        self.favorite_method = favorite_method
        self.favorite_type = favorite_type
        self.command = command
        self.prompt = prompt
        self.user_id = user_id
        
    def __repr__(self):
        f"Formel mit {self.favorite_method}, {self.favorite_type}, {self.command}, {self.prompt} wurde am {self.favorite_date} hinzugefügt."
