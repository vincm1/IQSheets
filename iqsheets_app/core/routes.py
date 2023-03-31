''' Core routes for landing page etc. '''
from flask import Blueprint, render_template

################
#### config ####
################

core_blueprint = Blueprint('core', __name__)

@core_blueprint.route("/")
@core_blueprint.route("/home")
def index():
    return render_template('index.html')

@core_blueprint.route("/abos")
def pricing():
    return render_template('pricing.html')