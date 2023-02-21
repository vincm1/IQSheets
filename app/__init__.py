from flask import Flask, render_template
from app.auth.routes import auth

app = Flask(__name__)

app.register_blueprint(auth)

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
