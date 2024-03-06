
''' Views for flask admin '''
import os
import boto3
import stripe
from datetime import datetime
import logging
from botocore.exceptions import ClientError
from flask import current_app, redirect, url_for, abort
from flask_login import current_user
from flask_admin import AdminIndexView, BaseView, expose
from iqsheets_app.admin.forms import TemplatesForm 
from flask_admin.contrib.sqla import ModelView 
from iqsheets_app import db
from iqsheets_app.models import Template

class MyAdminIndexView(AdminIndexView):
    ''' Index view for admin panel '''

    def is_accessible(self):
        # Check if the user is authenticated and is an admin
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

    def inaccessible_callback(self, name, **kwargs):
        ''' Redirect non-admin users to a 405 error page '''
        # If the user is not authenticated or not an admin, show a 405 error
        if not self.is_accessible():
            abort(403)  # Or redirect to a custom unauthorized access page
        return redirect(url_for('dashboard.dashboard'))

class UserView(ModelView):
    """ Admin View for loading user info """
    form_columns = ['id', 'username', 'email', 'job_description', 'profile_picture'
                    'registration_date', 'is_confirmed', 'confirmed_on', 'premium', 
                    'num_prompts', 'is_oauth']

class AnalyticsView(BaseView):
    """ Admin View for uploading Excel & Gsheet templates """
    @expose('/')
    def index(self):
        return self.render('admin/analytics_index.html')
    
class SubscriptionsView(BaseView):
    """ Admin View for uploading Excel & Gsheet templates """
    @expose('/')
    def index(self):
        if current_app.debug:
            stripe.api_key = current_app.config['STRIPE_SECRETKEY_TEST']
        else:
            stripe.api_key = current_app.config['STRIPE_SECRETKEY_PROD']
        customers = stripe.Customer.list()
        subscriptions = stripe.Subscription.list()
        return self.render('admin/subscriptions.html', customers=customers, subscriptions=subscriptions)

class TemplatesUploadView(BaseView):
    """ Admin View for uploading Excel & Gsheet templates """
    @expose('/', methods=["GET", "POST"])
    def index(self):
        # initialize S3 client using boto3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=current_app.config['AWS_REGION']
        )
        
        form = TemplatesForm()

        if form.validate_on_submit():
            file = form.template_name.data  # Access the file object directly from the form
            filename = file.filename
            folder = 'templates/'
            file_name = folder + filename
            
            try:
                # Upload file to S3
                s3_client.upload_fileobj(file, current_app.config["S3_BUCKET"], file_name)
            except ClientError as e:
                logging.error(e)
                return False

            # Commit Template to database
            file_db = Template(
                template_name=filename,
                template_category=form.template_category.data,
                template_description=form.template_description.data,
                folder=folder,
                bucket=current_app.config['S3_BUCKET'],
                region=current_app.config['AWS_REGION']
            )
            db.session.add(file_db)
            db.session.commit()

            return redirect(url_for('admin.index'))

        return self.render('admin/template_upload.html', form=form)