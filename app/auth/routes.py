from flask import Flask, Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required

auth = Blueprint('auth', __name__)

@auth.route("/registrieren")
def user_signup():
    return render_template('signup.html')

@auth.route("/login")
def user_login():
    return render_template('login.html')