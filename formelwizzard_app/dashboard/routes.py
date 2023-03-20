"""Routes for dashboard"""
from flask import Blueprint, render_template, flash, send_file, redirect, url_for, request
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
    print(form.data)
    if form.validate_on_submit():
        print(form)
        prompt = form.formula_explain.data + " " + form.excel_google.data + form.info_prompt.data + ": " + form.prompt.data
        print(prompt)
        result = openai_chat(prompt)
        print(result)
        # Increasing the amount of prompts and total tokens when prompt is generated
        current_user.num_prompts += 1
        current_user.num_tokens += result["usage"]["total_tokens"]
        # Commiting numbers to db
        db.session.commit()
        
        # Converting OpenAi prompt to a usable text
        explanation = result["choices"][0]["text"]
        print(explanation)
        # Converting OpenAi prompt to a usable text and formula if "formula selected" 
        text = result["choices"][0]["text"]
        start = text.find("=")
        end = text.find(")")
        formula = text[start:end+1]

        return render_template('dashboard/dashboard.html', form=form, form_2=form_2, explanation=explanation, formula=formula)
 
    return render_template('dashboard/dashboard.html', form=form, form_2=form_2)

@dashboard_blueprint.route('/<username>/favorites', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def favorites(username):
    """User favorite Excel Formulas"""
    print(request.args.get)
    page = request.args.get('page', 1, type=int)
    favorite_formulas = Favorite.query.filter_by(user_id=current_user.id).order_by(Favorite.favorite_date).paginate(page=page, per_page=9)
    return render_template('dashboard/favorites.html', favorite_formulas=favorite_formulas)

@dashboard_blueprint.route('/add_favorite', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def add_favorite():
    """Add Formula/VBA to User favorites"""
    form = FavoritesForm()
    if form.validate_on_submit():
        favorite = Favorite(user_id=current_user.id, provider=form.provider.data, favorite_type=form.favorite_type.data,
                           method=form.method.data, command=form.command.data, prompt=form.prompt.data)
        if favorite.provider:
            db.session.add(favorite)
            db.session.commit()
        else:
            redirect(url_for('dashboar.dashboard'))
        return redirect(url_for('dashboard.favorites', username=current_user.username))
    return redirect(url_for('dashboard.favorites', username=current_user.username))

@dashboard_blueprint.route('/formel_<int:favorite_id>/delete', methods=['GET'])
@login_required
@check_confirmed_mail
def delete_favorite(favorite_id):
    """Delete Formula/VBA to User favorites"""
    favorite = Favorite.query.filter_by(id=favorite_id).first()
    db.session.delete(favorite)
    db.session.commit()
    flash('Formel erfolgreich gelöscht!', 'success')
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
