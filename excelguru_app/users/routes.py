from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from excelguru_app import db
from excelguru_app.models import User
from excelguru_app.users.forms import RegistrationForm, LoginForm, EditUserForm

users = Blueprint('users', __name__)

@users.route('/signup', methods=['GET', 'POST'])
def signup_user():
    """Signigup User"""
    form = RegistrationForm()
    
    if form.validate_on_submit() and request.method == "POST":
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        
        flash('Erfolgreich angemeldet', 'success')
        return redirect(url_for('users.login_user'))
    
    return render_template('users/signup.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    """Login User"""
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Falscher Username oder Passwort')
            return redirect(url_for('users.user_login'))
        login_user(user, remember=True)
        return redirect(url_for('users.dashboard'))
    
    return render_template('users/login.html', form=form)

@login_required
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@users.route('/edit_profil')
def edit_user():
    user = User.query.filter_by(username=current_user.username).first()
    form = EditUserForm()
    
    return render_template('users/profil.html', form=form)

@login_required
@users.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """User Dashboard page"""
    return render_template('users/dashboard.html')