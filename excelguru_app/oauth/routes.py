from flask import Flask, Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required

oauth = Blueprint('oauth', __name__)

@oauth.route("/registrieren")
def oauth_signup():
    pass

@oauth.route("/oauth_login")
def oauth_login():
    pass