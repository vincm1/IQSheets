from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app,db)

### Flask Login Manager  ###
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "google.login"

mail = Mail(app)

### Blueprints ###
from excelguru_app.user.routes import user_blueprint
from excelguru_app.oauth.routes import oauth_blueprint

### Registering all Blueprints ###
app.register_blueprint(oauth_blueprint, url_prefix='/login')
app.register_blueprint(user_blueprint)

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
