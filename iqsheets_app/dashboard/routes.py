"""Routes for dashboard"""
from flask import Blueprint, current_app, render_template, flash, send_file, redirect, url_for, request
from flask_login import login_required, current_user
from iqsheets_app import db
from iqsheets_app.models import Prompt, Template
from iqsheets_app.utils.decorators import check_confirmed_mail
from iqsheets_app.openai import openai_chat
from .forms import DashboardForm, FavoritesForm
import boto3



################
#### config ####
################

dashboard_blueprint = Blueprint('dashboard', __name__)

# initialize S3 client using boto3
s3_client = boto3.client(
    's3',
    aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
    aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
    region_name=current_app.config['AWS_REGION']
    )
        
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
    return render_template('dashboard/dashboard.html', form=form, form_2=form_2)

@dashboard_blueprint.route('/dashboard/formel', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def formel():
    """User Dashboard page"""
    form = DashboardForm()  
    form_2 = FavoritesForm()
    
    if form.validate_on_submit():
        prompt = form.formula_explain.data + " " + form.excel_google.data + form.info_prompt.data + ": " + form.prompt.data
        result = openai_chat(prompt)
        # Increasing the amount of prompts and total tokens when prompt is generated
        current_user.num_prompts += 1
        current_user.num_tokens += result["usage"]["total_tokens"]
        # Creating prompt instance
        prompt = Prompt(user_id = current_user.id, provider=form.excel_google.data, method=form.info_prompt.data,
                        request=form.formula_explain.data, command=form.prompt.data, prompt=result["choices"][0]["text"][1:])
        # Commiting prompt and numbers to db
        db.session.add(prompt)
        db.session.commit()        

        # Converting OpenAi prompt to a usable text
        explanation = result["choices"][0]["text"]
        print(explanation)
        # Converting OpenAi prompt to a usable text and formula if "formula selected" 
        text = result["choices"][0]["text"]
        formula = text[1:]

        return render_template('dashboard/dashboard.html', form=form, form_2=form_2, explanation=explanation, formula=formula)

    return render_template('dashboard/dashboard.html', form=form, form_2=form_2, explanation=explanation, formula=formula)

@dashboard_blueprint.route('/dashboard/formel_feedback', methods=['POST'])
@login_required
@check_confirmed_mail
def prompt_feedback():
    ''' handles user feedback per prompt '''
    if request.form['correct-btn'] == "correct-response":
        print()

    return redirect(url_for('dashboard.dashboard'))

@dashboard_blueprint.route('/favoriten', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def favorites():
    """User favorite Excel Formulas"""
    page = request.args.get('page', 1, type=int)
    favorite_formulas = Prompt.query.filter_by(user_id=current_user.id).order_by(Prompt.createad_at).paginate(page=page, per_page=9)
    
    if request.method == 'POST' and request.form['filter_value'] == "Alle":
    
        page = request.args.get('page', 1, type=int)
        favorite_formulas = Prompt.query.filter_by(user_id=current_user.id).order_by(Prompt.favorite_date).paginate(page=page, per_page=9)
    
    elif request.method == 'POST':
        filter_value = request.form['filter_value']
        page = request.args.get('page', 1, type=int)
        favorite_formulas = Prompt.query.filter_by(user_id=current_user.id, provider=filter_value).order_by(Prompt.favorite_date).paginate(page=page, per_page=9)
        
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
@login_required
@check_confirmed_mail
def templates():
    """ Route for templates """
    if not current_user.premium:
        templates = Template.query.order_by(Template.created_at).limit(3).all()
        categorys = db.session.query(Template.template_category).distinct().all()
        
    else:
        page = request.args.get('page', 1, type=int)
        templates = Template.query.order_by(Template.created_at).paginate(page=page, per_page=12)
        categorys = db.session.query(Template.template_category).distinct().all()
        
        if request.method == 'POST' and request.form['filter_value'] == "Alle":
        
            page = request.args.get('page', 1, type=int)
            templates = Template.query.order_by(Template.created_at).paginate(page=page, per_page=12)
        
        elif request.method == 'POST':
            filter_value = request.form['filter_value']
            page = request.args.get('page', 1, type=int)
            templates = Template.query.filter_by(template_category=filter_value).order_by(Template.created_at).paginate(page=page, per_page=9)
        
    return render_template('dashboard/templates.html', templates=templates, categorys=categorys)

@dashboard_blueprint.route('/download', methods=['GET'])
@login_required
@check_confirmed_mail
def download():
    """ Route for templates download """
    filename = 'static/xlxs_templates/Calendar-Template.xlsx'
    try:
        return send_file(filename)
    except Exception as e:
        return str(e)
        
@dashboard_blueprint.route('/premium', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def premium():
    return render_template('dashboard/premium.html')
