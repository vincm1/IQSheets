
''' Views for flask admin '''
import os
import boto3
import stripe
from datetime import datetime
from botocore.exceptions import ClientError
from flask import current_app, redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView, BaseView, expose
from iqsheets_app.admin.forms import TemplatesForm 
from flask_admin.contrib.sqla import ModelView 
from iqsheets_app import db
from iqsheets_app.models import Template

class MyAdminIndexView(AdminIndexView):
    ''' Index view for admin panel '''
    def is_accessible(self):
        return current_user.is_admin
    
    def inacessible_callback(self, name, **kwargs):
        ''' Check if current user is admin '''
        print("here")
        return redirect(url_for('dashboard.dashboard'))

class UserView(ModelView):
    form_columns = ['id', 'username', 'email', 'job_description', 'profile_picture'
                    'registration_date', 'is_confirmed', 'confirmed_on', 'premium', 
                    'num_prompts', 'is_oauth']

class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/analytics_index.html')
    
class SubscriptionsView(BaseView):
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
    @expose('/', methods=["GET","POST"])
    def index(self):
        
        # initialize S3 client using boto3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=current_app.config['AWS_REGION']
        )
        
        print(s3_client.list_buckets())
        
        form = TemplatesForm()
        folder = 'templates/'
        
        if form.validate_on_submit():
            file_db = Template(template_name=form.data['template_name'].filename, 
                               template_category=form.data['template_category'],
                               template_description=form.data['template_description'],
                               folder=folder, bucket=current_app.config['S3_BUCKET'], 
                               region=current_app.config['AWS_REGION'])
            
            ### Boto3 Aws ###
            file = form.data['template_name']
            filename = form.data['template_name'].filename

            # Upload the file
            # initialize S3 client using boto3
            s3_client = boto3.client(
                's3',
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
                aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
                region_name=current_app.config['AWS_REGION']
            )
        
            try:
                response = s3_client.upload_file(file, current_app.config['S3_BUCKET'], folder + filename)
            except ClientError as e:
                logging.error(e)
                return False
            return True
        
            ### Committing Template to database ###
            db.session.add(file_db)
            db.session.commit()
            
            return redirect(url_for('admin.index'))
        
        return self.render('admin/template_upload.html', form=form)