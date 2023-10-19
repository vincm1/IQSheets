"""Flask configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

basedir = basedir = os.path.abspath(os.path.join('../', os.path.dirname(__file__)))

# create superclass
class BaseConfig(object):
    FLASK_APP = 'iqsheets_app'
    SECRET_KEY = os.getenv('SECRET_KEY')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    S3_BUCKET = os.getenv('S3_BUCKET')
    MAILCHIMP_AUDIENCE_ID =  os.getenv('MAILCHIMP_AUDIENCE_ID')
    MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
    MAILCHIMP_SERVERPREFIX = os.getenv('MAILCHIMP_SERVERPREFIX')
    LINKEDIN_OAUTH_CLIENT_ID = os.getenv('LINKEDIN_OAUTH_CLIENT_ID')
    LINKEDIN_OAUTH_CLIENT_SECRET = os.getenv('LINKEDIN_OAUTH_CLIENT_SECRET')
    FACEBOOK_OAUTH_CLIENT_ID = os.getenv('FACEBOOK_OAUTH_CLIENT_ID')
    FACEBOOK_OAUTH_CLIENT_SECRET = os.getenv('FACEBOOK_OAUTH_CLIENT_SECRET')
    KONTAKT_IQSHEETS = os.getenv('KONTAKT_IQSHEETS')
    
# Create the development config
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT ')
    db_user = os.getenv('DB_USER')
    db_pw = os.getenv('DB_PW')
    db_uri = os.getenv('DB_URI')
    db_url = f"postgresql+psycopg2://{db_user}:{db_pw}{db_uri}"
    SQLALCHEMY_DATABASE_URI = db_url
    #Admin settings
    ADMIN_USER = os.getenv('ADMIN_USER')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PW = os.getenv('ADMIN_PW')
    # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # gmail authentication
    MAIL_USERNAME = os.getenv('APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('APP_MAIL_PASSWORD')
    # mail accounts
    MAIL_DEFAULT_SENDER = os.getenv('APP_MAIL_USERNAME')
    #Oauth
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

# Create the testing config
class TestingConfig(BaseConfig):
    db_user = os.getenv('DB_USER')
    db_pw = os.getenv('DB_PW')
    db_uri = os.getenv('TEST_DB_URI')
    db_url = f"postgresql+psycopg2://{db_user}:{db_pw}{db_uri}"
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    ENV = 'testing'

# create the production config
class ProductionConfig(BaseConfig):
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}