""" Module for decorator functions """
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user, login_user
from iqsheets_app.models import db

def check_confirmed_mail(func):
    """ Route decorator to check user verified email """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_confirmed is False:
            flash('Bitte bestätige deine Anmeldung!', 'warning')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

def check_payment_oauth(func):
    """ Route decorator to check payments by oauth user """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        stripe_link = f"https://buy.stripe.com/test_aEU7t68NY7Dm6ukbIL?prefilled_email={current_user.email}"
        if current_user.stripe_customer_id and current_user.stripe_sub_id:
            login_user(current_user, remember=True)
            return redirect(url_for('dashboard.dashboard'))
        else:
            stripe_customer_id, stripe_subscription_id = current_user.check_payment()
            current_user.stripe_customer_id = stripe_customer_id
            current_user.stripe_sub_id = stripe_subscription_id
            db.session.add(current_user)
            db.session.commit()
            login_user(current_user, remember=True)
            return redirect(url_for('dashboard.dashboard'))
        return func(*args, **kwargs)

    return decorated_function

def non_oauth_required(func):
    """ Route decorator to show routes to non-oauth users only """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_oauth:
            return redirect(url_for('dashboard.dashboard'))  # Leite zu einer anderen Seite um
        return func(*args, **kwargs)
    return decorated_function