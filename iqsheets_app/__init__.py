''' Init file for app '''
import os
import logging
from datetime import timedelta
import datetime as time
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask.logging import default_handler
from werkzeug.security import generate_password_hash
from apscheduler.schedulers.background import BackgroundScheduler
from config import config
from .extensions import db, migrate, login_manager, mail, scheduler
from .admin.admin import create_admin, create_admin_user
from .user.email import send_reminder_unconfirmed_email

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
    login_manager.login_message = "Bitte logge dich ein."
    login_manager.login_message_category = "warning"
    
    # Flask Mail Instance
    mail.init_app(app)

    # Flask Admin instantiation
    create_admin(db).init_app(app)
    
    scheduler.init_app(app)
    
    # Set the duration for the remember cookie
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=3)
    
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
        
        # FlaskScheduler
        scheduler.start()
        def print_scheduler():
            print('Scheduler is running')
        scheduler.add_job(id="1", func=send_reminder_unconfirmed_email, trigger='interval', days=3)
        
        # Check if the database needs to be initialized
        engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        inspector = db.inspect(engine)
        if not inspector.has_table("users"):
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
        else:
            app.logger.info('Database already contains the users table.')
 
        ### Create admin user ###
        admin_user = User.query.filter_by(email=os.environ.get('ADMIN_EMAIL')).first()
        if not admin_user:
            create_admin_user(email=os.environ.get('ADMIN_EMAIL'),
                              password=generate_password_hash((os.environ.get('ADMIN_EMAIL'))))

        # Log mode of app
        app.logger.info(f"{app.debug}")
        logging.getLogger("apscheduler").setLevel(logging.INFO)
        
        return app

def configure_logging(app):
    # Logging Configuration
    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler = RotatingFileHandler('instance/flask-user-management.log',
                                           maxBytes=16384,
                                           backupCount=20)
        file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    app.logger.info('Starting the Flask User Management App...')
