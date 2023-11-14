from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def check_confirmed_mail(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_confirmed is False:
            flash('Bitte bestätige deine Anmeldung!', 'warning')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

def check_payment_oauth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        stripe_link = f"https://buy.stripe.com/test_aEU7t68NY7Dm6ukbIL?prefilled_email={current_user.email}"
        if current_user.stripe_customer_id is None and current_user.stripe_sub_id is None:
            return redirect(stripe_link)
        return func(*args, **kwargs)

    return decorated_function