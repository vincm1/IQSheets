from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app(config=DevelopmentConfig):
    '''Factory to create Flask application'''
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    ### Flask Login Manager  ###
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = "google.login"
    
    # Flask Mail Instance
    mail.init_app(app)

    with app.app_context():
        ### Blueprints ###
        from formelwizzard_app.core.routes import core_blueprint
        from formelwizzard_app.errors.routes import error_handlers_blueprint
        from formelwizzard_app.user.routes import user_blueprint
        from formelwizzard_app.oauth.routes import oauth_blueprint
        from formelwizzard_app.dashboard.routes import dashboard_blueprint

        ### Registering all Blueprints ###
        app.register_blueprint(core_blueprint)
        app.register_blueprint(error_handlers_blueprint)
        app.register_blueprint(oauth_blueprint, url_prefix='/login')
        app.register_blueprint(user_blueprint)
        app.register_blueprint(dashboard_blueprint)

        return app