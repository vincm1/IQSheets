
''' Views for flask admin '''
import os
import boto3
import stripe
from datetime import datetime
from flask import current_app, redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView, BaseView, expose
from iqsheets_app.admin.forms import TemplatesForm 
from flask_admin.contrib.sqla import ModelView 
from iqsheets_app import db
from iqsheets_app.models import Template

stripe.api_key = "sk_test_51MpD8VHjForJHjCtVZ317uTWseSh0XxZkuguQKo9Ei3WjaQdMDpo2AbKIYPWl2LXKPW3U3h6Lu71E94Gf1NvrHKE00xPsZzRZZ"
class MyAdminIndexView(AdminIndexView):
    ''' Index view for admin panel '''
    def is_accessible(self):
        return True
    
    def inacessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('user.login'))

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
            
            s3_client.upload_fileobj(file, current_app.config['S3_BUCKET'], folder + filename)
            
            ### Committing Template to database ###
            db.session.add(file_db)
            db.session.commit()
            
            return redirect(url_for('admin.index'))
        
        return self.render('admin/template_upload.html', form=form)