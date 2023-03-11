"""Routes for dashboard"""
from datetime import datetime
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from excelguru_app import app, db, mail
from excelguru_app.models import Favorite
from excelguru_app.utils.decorators import check_confirmed_mail
from excelguru_app.openai import openai_chat
from .forms import DashboardForm, FavoritesForm

################
#### config ####
################

dashboard_blueprint = Blueprint('dashboard', __name__)

################
#### routes ####
################

@dashboard_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def dashboard():
    """User Dashboard page"""
    form = DashboardForm()  
    form_2 = FavoritesForm()
    
    if form.validate_on_submit():
        prompt = "Excel " + form.info_prompt.data + ": " + form.prompt.data
        print(prompt)
        result = openai_chat(prompt)
        print(result)
        answer = result["choices"][0]["text"]
        
        start = answer.find("=")
        end = answer.find(")")
        
        formula = answer[start:end + 1]
        
        form_2 = FavoritesForm()
              
        if form_2.validate_on_submit and request.method=="POST":
            favorite = Favorite(favorite_method="Excel", favorite_type=form.info_prompt.data,
                                command=prompt, prompt=answer, user_id=current_user.id)
            db.session.add(favorite)
            db.session.commit()
        
        return render_template('dashboard/dashboard.html', form=form, form_2=form_2, result=result, answer=answer, formula=formula)
       
    return render_template('dashboard/dashboard.html', form=form, form_2=form_2)

@dashboard_blueprint.route('/<username>/favorites', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def favorites(username):
    """User favorite Excel Formulas"""
       
    return render_template('user/favorites.html')

@dashboard_blueprint.route('/templates', methods=['GET', 'POST'])
def templates():
    return render_template('dashboard/templates.html')


@dashboard_blueprint.route('/add_favorite', methods=['POST'])
@login_required
@check_confirmed_mail
def add_favorite():
    """Add Formula/VBA to User favorites"""
    

    return render_template("dashboard/dashboard.html")