""" Google Oauth routes """
from datetime import datetime
from flask import current_app, flash, url_for, redirect
from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from iqsheets_app.models import db, User, OAuth

google_blueprint = make_google_blueprint(
    client_id=current_app.config['GOOGLE_OAUTH_CLIENT_ID'],
    client_secret=current_app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="error")
        return False

    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False

    google_info = resp.json()
    google_user_id = google_info["id"]   
    
    # Check if the Google email is already associated with an account
    existing_user = User.query.filter_by(email=google_info['email']).first()
    
    if existing_user:
        # Find or create the OAuth token for the user
        oauth = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=google_user_id).first()
        
        if not oauth:
            # Create a new OAuth token for the existing user
            oauth = OAuth(provider=blueprint.name, provider_user_id=google_user_id, provider_user_email=google_info["email"], token=token)
            oauth.user = existing_user
            oauth.user.is_oauth = True
            db.session.add_all([existing_user, oauth])
            db.session.commit()

        # Log in the existing user
        login_user(existing_user, remember=True)
        return redirect(url_for('dashboard.dashboard'))
    else:
        # Create a new OAuth token for the user
        oauth = OAuth(provider=blueprint.name, provider_user_id=google_user_id, provider_user_email=google_info["email"], token=token)

        # Create a new local user account for this user
        user = User(username=google_info["name"], email=google_info["email"], password="")
        # Associate the new local user account with the OAuth token
        oauth.user = user
        user.is_confirmed = True
        user.confirmed_on = datetime.utcnow()
        user.is_oauth = True
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('dashboard.dashboard'))

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

# notify on OAuth provider error
@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")