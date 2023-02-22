from flask import Flask, Blueprint, render_template, redirect, session, request, flash
from excelguru_app import db
from excelguru_app.models import User
from flask_login import login_user, login_required, logout_user, current_user
from excelguru_app.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)

@users.route('/signup', methods=['GET', 'POST'])
def signup_user():
    form = RegistrationForm()
    
    if form.validate_on_submit() and request.method == "POST":
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        
        flash('Erfolgreich angemeldet', 'success')
        return redirect(url_for('users.login_user'))
    
    return render_template('users/signup.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login_user():
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Falscher Username oder Passwort')
            return redirect(url_for('users.user_login'))
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('users/login.html', form=form)

@login_required
@users.route('/dashboard', methods=['GET', 'POST'])
def dashboard_user():
    return render_template('users/dashboard.html')