''' Extensions for App ''' 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_apscheduler import APScheduler

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
scheduler = APScheduler()
