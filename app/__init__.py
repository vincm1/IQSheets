from flask import Flask, render_template
from app.auth.routes import auth

app = Flask(__name__)

app.register_blueprint(auth)

@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')


