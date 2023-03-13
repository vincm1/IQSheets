"""Routes for user"""
import os
from datetime import datetime
from flask import Blueprint, current_app, render_template, redirect, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from excelguru_app import app, db, mail
from excelguru_app.models import User
from .forms import RegistrationForm, LoginForm, EditUserForm, ResetPasswordRequestForm, ResetPasswordForm
from .token import generate_confirmation_token, confirm_token
from .email import send_email
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
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
                    password=form.password.data, job_description=None, is_confirmed=False)

        db.session.add(user)
        db.session.commit()
        
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('user/email/activate.html', confirm_url=confirm_url)
        subject = "Bitte bestätige Deine Email für ExcelWizzard!"
        send_email(user.email, subject, html)
        
        flash(f'Eine Bestätigungs-Email wurde an {user.email} geschickt.', 'success')
        return redirect(url_for('user.login'))
    
    return render_template('user/signup.html', form=form)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login User"""
    form = LoginForm()
    form_2 = ResetPasswordForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Falscher Username oder Passwort')
            return redirect(url_for('user.login'))
        login_user(user, remember=True)
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('user/login.html', form=form)

@user_blueprint.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    return redirect(url_for('index'))

@user_blueprint.route('/confirm/<token>')
def confirm_email(token):
    
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    
    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Account bestätigt', 'success')
        return redirect(url_for('user.login'))
    else:
        flash('Der Bestätigungslink ist abgelaufen oder invalide.', 'danger')
    return redirect(url_for('index'))

@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.is_confirmed:
        return redirect('user.login')
    flash('Bitte Account bestätigen', 'warning')
    return render_template('user/unconfirmed.html')

@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/email/activate.html', confirm_url=confirm_url)
    subject = "Bitte bestätige Deine Email für ExcelWizzard!"
    send_email(current_user.email, subject, html)
    flash(f'Eine Bestätigungs-Email wurde an {current_user.email} geschickt.', 'success')
    return redirect(url_for('user.unconfirmed'))

@user_blueprint.route('/edit_profil', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def edit_user():
    """Edit user profile"""
    user = User.query.filter_by(username=current_user.username).first()
    form = EditUserForm()
    
    if form.validate_on_submit():
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.job_description = form.job_description.data
        current_user.profile_picture = form.profile_picture.data
        # Image name
        pic_filename = secure_filename(current_user.profile_picture.filename)
        # UUID
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        current_user.profile_picture.save(os.path.join(current_app.root_path, 'static/profile_pictures', pic_name))
        current_user.profile_picture = pic_name
       
        db.session.add(user)
        db.session.commit()
        flash("Profil erfolgreich bearbeitet!", "success")
        return render_template('user/profil.html', form=form)
    
    return render_template('user/profil.html', form=form)

@user_blueprint.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_confirmed:
            
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('user.reset_password', token=token, _external=True)
            subject = f"Passwort Reset für {user.username} ExcelWizzard!"
            html = render_template('user/email/reset_password.html', confirm_url=confirm_url)
            send_email(user.email, subject, html)
            flash('Prüfe deine Emails', 'success')
        else:
            flash('Noch nicht verifiziert', 'info')
            return redirect(url_for('user.unconfirmed'))
    return render_template('user/reset_password_request.html',
                           title='Passwort zurücksetzen', form=form)
    
@user_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = confirm_token(token)
    
    user = User.query.filter_by(email=email).first_or_404()
    
    if not user:
        return redirect(url_for('index'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Passwort zurückgesetzt', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/reset_password.html', form=form)



