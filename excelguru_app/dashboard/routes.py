from datetime import datetime
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from excelguru_app import app, db, mail
from excelguru_app.models import User


################
#### config ####
################

dashboard_blueprint = Blueprint('dashboard', __name__)

################
#### routes ####
################

@dashboard_blueprint.route('/templates', methods=['GET', 'POST'])
def templates():
    
    return render_template('dashboard/templates.html')