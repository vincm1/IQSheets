"""Flask configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

basedir = basedir = os.path.abspath(os.path.join('../', os.path.dirname(__file__)))

# create superclass
class BaseConfig(object):
    ''' Config base '''
    FLASK_APP = 'iqsheets_app'
    SECRET_KEY = os.getenv('SECRET_KEY')
    #AWS
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    #Admin settings
    ADMIN_USER = os.getenv('ADMIN_USER')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PW = os.getenv('ADMIN_PW')
    # MAIL SETTINGS
    MAIL_SERVER = 'mail.privateemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # PRIVATEEMAIL SETTINGS (NAMECHEAP)
    MAIL_USERNAME = os.getenv('KONTAKT_IQSHEETS')
    MAIL_PASSWORD = os.getenv('APP_MAIL_PASSWORD')
    # mail accounts
    MAIL_DEFAULT_SENDER = os.getenv('KONTAKT_IQSHEETS')
    #MAILCHIMP
    MAILCHIMP_AUDIENCE_ID =  os.getenv('MAILCHIMP_AUDIENCE_ID')
    MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
    MAILCHIMP_SERVERPREFIX = os.getenv('MAILCHIMP_SERVERPREFIX')
    #OAUTH
    GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    LINKEDIN_OAUTH_CLIENT_SECRET = os.getenv('LINKEDIN_OAUTH_CLIENT_SECRET')
    LINKEDIN_OAUTH_CLIENT_ID = os.getenv('LINKEDIN_OAUTH_CLIENT_ID')
    LINKEDIN_OAUTH_CLIENT_SECRET = os.getenv('LINKEDIN_OAUTH_CLIENT_SECRET')
    FACEBOOK_OAUTH_CLIENT_ID = os.getenv('FACEBOOK_OAUTH_CLIENT_ID')
    FACEBOOK_OAUTH_CLIENT_SECRET = os.getenv('FACEBOOK_OAUTH_CLIENT_SECRET')
    #Other
    KONTAKT_IQSHEETS = os.getenv('KONTAKT_IQSHEETS')
    LOG_WITH_GUNICORN = os.getenv('LOG_WITH_GUNICORN', default=False)    
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    
# Create the development config
class DevelopmentConfig(BaseConfig):
    ''' Config for development '''
    DEBUG = True
    FLASK_ENV = 'development'
    db_user = os.getenv('DB_USER')
    db_pw = os.getenv('DB_PW')
    db_uri = os.getenv('DB_URI')
    db_url = f"postgresql+psycopg2://{db_user}:{db_pw}{db_uri}"
    SQLALCHEMY_DATABASE_URI = db_url
    #Stripe
    STRIPE_PUBLIC_KEY_TEST = os.environ.get('STRIPE_PUBLIC_KEY_TEST')
    STRIPE_SECRETKEY_TEST = os.environ.get('STRIPE_SECRETKEY_TEST')
    #Oauth
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    #Stripe test keys
    STRIPE_PUBLIC_KEY_TEST = os.environ.get('STRIPE_PUBLIC_KEY_TEST')
    STRIPE_SECRETKEY_TEST = os.environ.get('STRIPE_SECRETKEY_TEST')
    # Amazon S3
    S3_BUCKET = os.getenv('S3_BUCKET_DEV')

# Create the testing config
class TestingConfig(BaseConfig):
    ''' Test config '''
    db_user = os.getenv('DB_USER')
    db_pw = os.getenv('DB_PW')
    db_uri = os.getenv('TEST_DB_URI')
    db_url = f"postgresql+psycopg2://{db_user}:{db_pw}{db_uri}"
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    FLASK_ENV = 'testing'

# create the production config
class ProductionConfig(BaseConfig):
    ''' Production config '''
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = 'production'
    S3_BUCKET = os.getenv('S3_BUCKET')
    STRIPE_PUBLIC_KEY_PROD = os.environ.get('STRIPE_PUBLIC_KEY_PROD')
    STRIPE_SECRETKEY_PROD = os.environ.get('STRIPE_SECRETKEY_PROD')
    

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}