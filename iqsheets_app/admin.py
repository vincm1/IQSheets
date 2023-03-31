from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView  
from .models import User, OAuth, Favorite

def create_admin(db):
    admin = Admin(name="IQSheet Admin", template_mode="bootstrap4")
    
    # Add views
    admin.add_view(ModelView(User, db.session, endpoint="users_admin"))
    admin.add_view(ModelView(OAuth, db.session, endpoint="oauth_admin"))
    admin.add_view(ModelView(Favorite, db.session))

    return admin