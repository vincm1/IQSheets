"""Routes for user"""
import os
from datetime import datetime
import boto3
from flask import Blueprint, Markup, current_app, render_template, redirect, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from iqsheets_app import db, mail
from iqsheets_app.models import User
from .forms import RegistrationForm, LoginForm, EditUserForm, ChangePasswordForm, ResetPasswordRequestForm, ResetPasswordForm
from .token import generate_confirmation_token, confirm_token
from .email import send_email
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
from flask_mail import Message
from iqsheets_app.utils.decorators import check_confirmed_mail
from iqsheets_app.openai import openai_chat
from iqsheets_app.core.forms import NewsletterForm

################
#### config ####
################

user_blueprint = Blueprint('user', __name__)

################
#### routes ####
################

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """ Registering a local user """
    form = RegistrationForm()
    form_nl = NewsletterForm()
    
    if form.validate_on_submit() and request.method == "POST":
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('user/email/activate.html', confirm_url=confirm_url)
        subject = "Bitte bestätige Deine Email für IQSheets!"
        send_email(user.email, subject, html)
        
        flash(f'Eine Bestätigungs-Email wurde an {user.email} geschickt.', 'success')
        return redirect(url_for('user.login'))
    
    return render_template('user/signup.html', form=form, form_nl=form_nl)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login User"""
    form = LoginForm()
    form_2 = ResetPasswordForm()
    form_nl = NewsletterForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Check if user exist
        if user:
            # Check if user confirmed registration link
            if user.is_confirmed:
                # Check password of user
                if user.check_password(form.password.data):
                    if user.is_admin:
                        login_user(user, remember=True)
                        return redirect(url_for('dashboard.dashboard'))
                    else:
                        user.check_payment()
                        if user.stripe_customer_id and user.stripe_sub_id is not None:
                            login_user(user, remember=True)
                            return redirect(url_for('dashboard.dashboard'))
                        else:
                            flash(Markup('Kontaktiere unseren Support - <a href="{{url_for("core.index")}}">Supportseite</a>'), 'danger')
                            return redirect(url_for('user.login'))    
                else:
                    flash('Prüfe deine Anmeldedaten!', 'danger')
                    return redirect(url_for('user.login'))
            else:
                flash('Bitte bestätige deine Anmeldung per Link', 'danger')
        else:
            flash('Prüfe deine Anmeldedaten!', 'danger')
            return redirect(url_for('user.login'))
    return render_template('user/login.html', form=form, form_2=form_2, form_nl=form_nl)    

@user_blueprint.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    return redirect(url_for('core.index'))

@user_blueprint.route('/confirm/<token>')
def confirm_email(token):
    """ Sending confirmation Email to user after signup """
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()
    print(user.email)
    form_nl = NewsletterForm()
    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Account bestätigt', 'success')
        stripe_link = f"https://buy.stripe.com/test_aEU7t68NY7Dm6ukbIL?prefilled_email={user.email}&prefilled_benutzername={user.username}"
        return redirect(stripe_link)
        # return render_template('stripe/checkout.html', user_email=email, form_nl=form_nl)
    else:
        flash('Der Bestätigungslink ist abgelaufen oder invalide.', 'danger')
    return redirect(url_for('core.index'))

@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    """ Checking if user confirmed email link """
    if current_user.is_confirmed:
        return redirect('user.login')
    flash('Bitte Account bestätigen', 'warning')
    return render_template('user/unconfirmed.html')

@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    """ Resending a confirmation link after signup """
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/email/activate.html', confirm_url=confirm_url)
    subject = "Bitte bestätige Deine Email für IQSheets!"
    send_email(current_user.email, subject, html)
    flash(f'Eine Bestätigungs-Email wurde an {current_user.email} geschickt.', 'success')
    return redirect(url_for('user.unconfirmed'))

@user_blueprint.route('/profil_bearbeiten', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def edit_user():
    """Edit user profile"""
    
    # initialize S3 client using boto3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'], 
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['AWS_REGION']
        )
    
    user = User.query.filter_by(username=current_user.username).first()
    form = EditUserForm()
    
    folder = 'profile_pictures/'
    
    if form.validate_on_submit():
        for field in ['username', 'email', 'job_description']:
            if getattr(form, field).data and getattr(current_user, field) != getattr(form, field).data:
                setattr(current_user, field, getattr(form, field).data)
                
        if form.data['profile_picture'] and current_user.profile_picture !=  form.data['profile_picture']:
            current_user.profile_picture = form.profile_picture.data
            # Image name
            pic_filename = secure_filename(current_user.profile_picture.filename)
            # UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            
            ### Boto3 Aws ###
            file = form.data['profile_picture']
            s3_client.upload_fileobj(file, current_app.config['S3_BUCKET'], folder + pic_name)
            current_user.profile_picture = pic_name
                
        else:
            current_user.profile_picture = current_user.profile_picture       
             
        db.session.add(user)
        db.session.commit()
        flash("Profil erfolgreich bearbeitet!", "success")
        return render_template('user/profil.html', form=form)
    
    return render_template('user/profil.html', form=form)

@user_blueprint.route('/passwort', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def change_password():
    """Edit user password"""
    user = User.query.filter_by(username=current_user.username).first()
    
    form = ChangePasswordForm()
    
    if form.validate_on_submit() and user.check_password(form.old_password.data):
        current_user.password_hash = generate_password_hash(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash("Passwort erfolgreich bearbeitet!", "success")
        return redirect(url_for('dashboard.dashboard'))
    else:
        flash("Altes Passwort stimmt nicht!", "warning")
    
    return render_template('user/password.html', form=form)

@user_blueprint.route('/<username>/payments', methods=['GET'])
@login_required
@check_confirmed_mail
def user_payments(username):
    """ User payments routes """
    return render_template('user/payments.html', username=current_user.username)

@user_blueprint.route('/passwort_zuruecksetzen', methods=['GET', 'POST'])
def reset_password_request():
    """ Sending a password request """
    form = ResetPasswordRequestForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_confirmed:
            
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('user.reset_password', token=token, _external=True)
            subject = f"Passwort Reset für {user.username} IQSheets!"
            html = render_template('user/email/reset_password.html', confirm_url=confirm_url)
            send_email(user.email, subject, html)
            flash('Prüfe deine Emails', 'success')
        else:
            flash('Kein Profil unter dieser Emailadresse', 'warning')
            #return redirect(url_for('core.index'))
    return render_template('user/reset_password_request.html',
                           title='Passwort zurücksetzen', form=form)
    
@user_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """ Resetting password after clicking on tokenized mail link """
    email = confirm_token(token)   
    user = User.query.filter_by(email=email).first_or_404()
    
    if not user:
        return redirect(url_for('core.index'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Passwort zurückgesetzt', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/reset_password.html', form=form)

