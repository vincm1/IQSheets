from datetime import datetime
from flask import current_app, flash, url_for, redirect
from flask_login import current_user, login_user
from flask_dance.contrib.linkedin import make_linkedin_blueprint, linkedin
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from iqsheets_app.models import db, User, OAuth

linkedin_blueprint = make_linkedin_blueprint(
    client_id=current_app.config['LINKEDIN_OAUTH_CLIENT_ID'],
    client_secret=current_app.config['LINKEDIN_OAUTH_CLIENT_SECRET'],
    scope=["r_liteprofile", "r_emailaddress"],
    redirect_url="http://127.0.0.1:5000/login/linkedin/authorized",
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(linkedin_blueprint)
def linkedin_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="error")
        return False

    resp = linkedin.get("me")
    email = linkedin.get('emailAddress?q=members&projection=(elements*(handle~))')
    
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False

    linkedin_info = resp.json()
    email = email.json()
    linkedin_email = email['elements'][0]['handle~']['emailAddress']
    linkedin_user_id = linkedin_info["id"]
    print(linkedin_email)
    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=linkedin_user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=linkedin_user_id, token=token)

    if oauth.user:
        login_user(oauth.user)
        return redirect(url_for('dashboard.dashboard'))

    else:
        # Create a new local user account for this user
        user = User(username=linkedin_info['localizedFirstName'] + " " + linkedin_info['localizedLastName'], 
                    email=linkedin_email, password="")
        # Associate the new local user account with the OAuth token
        oauth.user = user
        user.is_confirmed = True
        user.confirmed_on = datetime.utcnow()
        user.is_oauth = True
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        return redirect(url_for('dashboard.dashboard'))

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

# notify on OAuth provider error
@oauth_error.connect_via(linkedin_blueprint)
def linkedin_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")