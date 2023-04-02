
Views for flask admin 
import os
from flask_login import current_user
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView 
from .forms import TemplatesForm 

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == os.environ.get("ADMIN_USER") and current_user.is_admin
    
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

class TemplatesUploadView(BaseView):
    @expose('/', methods=["GET","POST"])
    def index(self):
        form = TemplatesForm()
        
        if form.validate_on_submit():
            pass
        
        return self.render('admin/template_upload.html', form=form)