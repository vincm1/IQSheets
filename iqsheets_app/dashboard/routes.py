"""Routes for dashboard"""
import boto3
from datetime import datetime
from flask import Blueprint, current_app, render_template, flash, send_file, redirect, url_for, request
from flask_login import login_required, current_user
from iqsheets_app import db
from iqsheets_app.models import Prompt, Template
from iqsheets_app.utils.decorators import check_confirmed_mail
from iqsheets_app.openai import openai_chat
from .forms import FormelForm, SkriptForm, SqlForm, RegExForm

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

@dashboard_blueprint.route('/dashboard', methods=['GET'])
@login_required
@check_confirmed_mail
def dashboard():
    """User Dashboard page"""
    return render_template('dashboard/dashboard.html')

@dashboard_blueprint.route('/<prompt_type>', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def prompter(prompt_type):
    """User Dashboard page"""
    valid_prompt_types = ["formula", "skripte", "sql", "regex"]
    if prompt_type not in valid_prompt_types:
    # Handle invalid prompt_type, maybe redirect to a default page or show an error
        return redirect(url_for('dashboard.dashboard'))
    if prompt_type == "formula":
        form = FormelForm()
    elif prompt_type == "skripte":
        form = SkriptForm()
    elif prompt_type == "sql":
        form = SqlForm()
    else:
        form = RegExForm()

    return render_template(f"dashboard/{prompt_type}_page.html", form=form)

@dashboard_blueprint.route('/<prompt_type>/result', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def formel(prompt_type):
    """User Dashboard page"""
    if prompt_type == "formula":
        form = FormelForm()
    elif prompt_type == "skripte":
        form = SkriptForm()
    elif prompt_type == "sql":
        form = SqlForm()
    else:
        form = RegExForm()
   
    if request.method == 'POST' and form.validate_on_submit():
        form_data = form.data
        form_data['prompt_type'] = prompt_type.capitalize()
        keys = ["prompt_type","excel_google", "vba_app", "formula_explain", "prompt"]
        prompt = []
        for key in keys:
            if key in form_data:
                prompt.append(form_data[key])
        # Form user info to prompt for OpenAI
        prompt = " ".join(prompt)
        result = openai_chat(prompt)
        answer = result.choices[0].message.content
        
        # Increasing the amount of prompts and total tokens when prompt is generated
        current_user.num_prompts += 1
        current_user.num_tokens += result.usage.total_tokens
    
        # Creating prompt instance
        prompt = Prompt(user_id = current_user.id, prompt_type=prompt_type.capitalize(), category=form.formula_explain.data,
                        prompt=form.prompt.data, result=answer)
        # Commiting prompt and numbers to db
        db.session.add(prompt)
        db.session.commit()
        
        return render_template(f'dashboard/{prompt_type}_page.html', answer=answer, form=form, prompt_id=prompt.id)

    return render_template(f'dashboard/{prompt_type}_page.html', form=form)

@dashboard_blueprint.route('/dashboard/favorite/<int:prompt_id>', methods=['GET'])
@login_required
@check_confirmed_mail
def prompt_favorite(prompt_id):
    ''' handles user feedback per prompt '''
    prompt = Prompt.query.filter_by(id=prompt_id).first()
    prompt.favorite = True
    db.session.commit()
    return redirect(url_for('dashboard.favorites'))

@dashboard_blueprint.route('/dashboard/negative/<int:prompt_id>', methods=['GET'])
@login_required
@check_confirmed_mail
def negative_feedback(prompt_id):
    ''' handles user feedback per prompt '''
    prompt = Prompt.query.filter_by(id=prompt_id).first()
    prompt.feedback = False
    db.session.commit()
    return redirect(request.referrer or '/default-page')

@dashboard_blueprint.route('/favoriten', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def favorites():
    """User favorite Excel Formulas"""
    page = request.args.get('page', 1, type=int)
    favorite_formulas = Prompt.query.filter_by(user_id=current_user.id, 
                                               favorite=True).order_by(Prompt.created_at).paginate(page=page, 
                                                                                                   per_page=30)
    # prompt_types = db.session.query(Prompt.prompt_type).distinct().all()
    prompt_types = ["formula", "skripte", "sql", "regex"]
    today = datetime.now()
    if request.method == 'POST' and request.form['filter_value'] == "Alle":
    
        page = request.args.get('page', 1, type=int)
        favorite_formulas = Prompt.query.filter_by(user_id=current_user.id, favorite=True).order_by(Prompt.created_at).paginate(page=page, per_page=9)
    
    elif request.method == 'POST':
        filter_value = request.form['filter_value']
        page = request.args.get('page', 1, type=int)
        favorite_formulas = Prompt.query.filter_by(user_id=current_user.id, favorite=True, 
                                                   prompt_type=filter_value).order_by(Prompt.created_at).paginate(page=page, per_page=30)
        
        
    return render_template('dashboard/favorites.html', favorite_formulas=favorite_formulas, prompt_types=prompt_types, today=today)

@dashboard_blueprint.route('/formel_<int:favorite_id>/delete', methods=['GET'])
@login_required
@check_confirmed_mail
def delete_favorite(favorite_id):
    """Delete Formula/VBA to User favorites"""
    favorite = Prompt.query.filter_by(id=favorite_id).first()
    db.session.delete(favorite)
    db.session.commit()
    flash('Favorit erfolgreich gelöscht!', 'success')
    return redirect(url_for('dashboard.favorites', username=current_user.username))

@dashboard_blueprint.route('/templates', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def templates():
    """ Route for templates """
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
