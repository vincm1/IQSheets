"""Routes for user"""
from datetime import datetime
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from excelguru_app import app, db, mail
from excelguru_app.models import User
from .forms import RegistrationForm, LoginForm, EditUserForm, DashboardForm
from .token import generate_confirmation_token, confirm_token
from .email import send_email
from flask_mail import Message
from excelguru_app.utils.decorators import check_confirmed_mail
from excelguru_app.openai import openai_chat

################
#### config ####
################

user_blueprint = Blueprint('user', __name__)

################
#### routes ####
################

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit() and request.method == "POST":
        user = User(username=form.username.data, email=form.email.data, 
                    password=form.password.data, is_confirmed=False)

        db.session.add(user)
        db.session.commit()
        
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Bitte bestätige Deine Email für ExcelWizzard!"
        send_email(user.email, subject, html)
        
        flash(f'Eine Bestätigungsemail wurde an {user.email} geschickt.', 'success')
        return redirect(url_for('user.login'))
    
    return render_template('user/signup.html', form=form)

@user_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
        
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        
    user = User.query.filter_by(email=email).first_or_404()
    
    if user.is_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    
    else:
        user.is_confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
        
    return redirect(url_for('index'))

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login User"""
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Falscher Username oder Passwort')
            return redirect(url_for('user.login'))
        login_user(user, remember=True)
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/login.html', form=form)

@user_blueprint.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    return redirect(url_for('index'))

@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.is_confirmed:
        return redirect('main.home')
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')

@user_blueprint.route('/edit_profil', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def edit_user():
    """Edit user profile"""
    user = User.query.filter_by(username=current_user.username).first()
    form = EditUserForm()
    
    return render_template('user/profil.html', form=form)

@user_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def dashboard():
    """User Dashboard page"""
    form = DashboardForm()
    
    if form.validate_on_submit():
        prompt = form.prompt.data
        result = openai_chat(prompt)
        
        answer = result["choices"][0]["text"]
        
        start = answer.find("=")
        end = answer.find(")")
        
        formula = answer[start:end + 1]
        
        return render_template('user/dashboard.html', form=form, answer=answer, formula=formula)
       
    return render_template('user/dashboard.html', form=form)
