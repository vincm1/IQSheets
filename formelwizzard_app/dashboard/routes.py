"""Routes for dashboard"""
from flask import Blueprint, render_template, request, send_file, redirect ,url_for
from flask_login import login_required, current_user
from formelwizzard_app import db
from formelwizzard_app.models import Favorite
from formelwizzard_app.utils.decorators import check_confirmed_mail
from formelwizzard_app.openai import openai_chat
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
    form_3 = FavoritesForm()
    
    if form.validate_on_submit():
        prompt = form.formula_explain.data + " " + form.excel_google.data + form.info_prompt.data + ": " + form.prompt.data
        
        result = openai_chat(prompt)
        # Increasing the amount of prompts and total tokens when prompt is generated
        current_user.num_prompts += 1
        current_user.num_tokens += result["usage"]["total_tokens"]
        # Commiting numbers to db
        db.session.commit()
        
        if form.formula_explain.data == "Erklären":
            explanation = result["choices"][0]["text"]

            return render_template('dashboard/dashboard.html', form=form, form_2=form_2, explanation=explanation)
        
        else:
        
            text = result["choices"][0]["text"]
            print(text)
            start = text.find("=")
            end = text.find(")")
            formula = text[start:end+1]
            print(formula)
                    
            return render_template('dashboard/dashboard.html', form=form, form_3=form_3, formula=formula)
       
    return render_template('dashboard/dashboard.html', form=form, form_2=form_2, form_3=form_3)

@dashboard_blueprint.route('/<username>/favorites', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def favorites(username):
    """User favorite Excel Formulas"""
    favorite_formulas = Favorite.query.filter_by(user_id=current_user.id).order_by(Favorite.favorite_date).all()
    return render_template('user/favorites.html', favorite_formulas=favorite_formulas)

@dashboard_blueprint.route('/add_favorite', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def add_favorite():
    """Add Formula/VBA to User favorites"""
    form_2 = FavoritesForm()
   
    # if form.validate_on_submit and request.method=="POST":
    #     favorite = Favorite(favorite_method=form.favorite_type.data, favorite_type=form.favorite_method.data,
    #                         command=form.command.data, prompt=form.prompt.data, user_id=current_user.id)
    #     print(favorite)
    return redirect(url_for('dashboard.favorites', username=current_user.username))

@dashboard_blueprint.route('/templates', methods=['GET', 'POST'])
def templates():
    """ Route for templates """
    return render_template('dashboard/templates.html')

@dashboard_blueprint.route('/download', methods=['GET'])
def download():
    """ Route for templates download """
    filename = 'static/xlxs_templates/Calendar-Template.xlsx'
    try:
        return send_file(filename)
    except Exception as e:
        return str(e)
        

@dashboard_blueprint.route('/premium', methods=['GET', 'POST'])
def premium():
    return render_template('dashboard/premium.html')
