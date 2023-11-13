''' Init file for app '''
import os
from flask import Flask, render_template
from config import config
from .extensions import db, migrate, login_manager, mail
from .admin.admin import create_admin, create_admin_user
from werkzeug.security import generate_password_hash

def create_app(config_name=None):
    '''Factory to create Flask application'''
    
    # check if config name is given
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")
    
    # instantiate the app
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    ### Flask Login Manager  ###
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'user.login'
    
    # Flask Mail Instance
    mail.init_app(app)

    # Flask Admin instantiation
    create_admin(db).init_app(app)
    
    from iqsheets_app.models import User
    
    with app.app_context():
        ### Blueprints ###
        from iqsheets_app.core.routes import core_blueprint
        from iqsheets_app.errors.routes import error_handlers_blueprint
        from iqsheets_app.user.routes import user_blueprint
        from iqsheets_app.oauth import google_blueprint, linkedin_blueprint, facebook_blueprint
        from iqsheets_app.dashboard.routes import dashboard_blueprint

        ### Registering all Blueprints ###
        app.register_blueprint(core_blueprint)
        app.register_blueprint(error_handlers_blueprint)
        app.register_blueprint(linkedin_blueprint, url_prefix="/login")
        app.register_blueprint(google_blueprint, url_prefix="/login")
        app.register_blueprint(facebook_blueprint, url_prefix="/login")
        app.register_blueprint(user_blueprint)
        app.register_blueprint(dashboard_blueprint)
        
        db.create_all()
        
        ### Create admin user ###
        admin_user = User.query.filter_by(username=os.environ.get('ADMIN_USER')).first()
        if not admin_user:
            create_admin_user(username=os.environ.get('ADMIN_USER'), email=os.environ.get('ADMIN_EMAIL'),
                              password=generate_password_hash((os.environ.get('ADMIN_EMAIL'))))

        return app