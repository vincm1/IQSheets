from dotenv import load_dotenv
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)

sec_key = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

### DB Config and migration ###
db_user = os.getenv('DB_USER')
db_pw = os.getenv('DB_PW')
db_uri = os.getenv('DB_URI')
db_url = f"postgresql+psycopg2://{db_user}:{db_pw}{db_uri}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

### Flask Login Manager  ###
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "users.login"

### Blueprints ###
from excelguru_app.users.routes import users
from excelguru_app.oauth.routes import oauth

### Registering all Blueprints ###
app.register_blueprint(oauth)
app.register_blueprint(users)

### Core Routes ###

@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')

@app.route("/preise")
def pricing():
    return render_template('pricing.html')

@app.route("/about")
def about():
    return render_template('about.html')
