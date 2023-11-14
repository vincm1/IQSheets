"""Routes for dashboard"""
from flask import Blueprint, current_app, render_template, flash, send_file, redirect, url_for, request
from flask_login import login_required, current_user
from iqsheets_app import db
from iqsheets_app.models import Prompt, Template
from iqsheets_app.utils.decorators import check_confirmed_mail, check_payment_oauth
from iqsheets_app.openai import openai_chat
from .forms import DashboardForm
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
    gif = 'static/img/beam-a-person-is-typing-on-a-laptop.gif'
    
    return render_template('dashboard/dashboard.html', form=form, gif=gif)

@dashboard_blueprint.route('/dashboard/formel', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def formel():
    """User Dashboard page"""
    form = DashboardForm()  
    gif = '../static/img/beam-a-person-is-typing-on-a-laptop.gif'
   
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
        
        return render_template('dashboard/dashboard.html', form=form, explanation=explanation, formula=formula, prompt=prompt, gif=gif)

    return render_template('dashboard/dashboard.html', form=form, gif=gif)

@dashboard_blueprint.route('/dashboard/favorite/<int:prompt_id>', methods=['POST'])
@login_required
@check_confirmed_mail
def prompt_favorite(prompt_id):
    ''' handles user feedback per prompt '''
    prompt = Prompt.query.filter_by(id=prompt_id).first()
    if request.form['favorite-btn'] == "favorite-prompt":
        prompt.favorite = True
        db.session.commit()
        return redirect(url_for('dashboard.favorites'))
    return redirect(url_for('dashboard.dashboard'))

@dashboard_blueprint.route('/dashboard/positive/<int:prompt_id>', methods=['POST'])
@login_required
@check_confirmed_mail
def positive_feedback(prompt_id):
    ''' handles user feedback per prompt '''
    prompt = Prompt.query.filter_by(id=prompt_id).first()
    if request.form['correct-btn'] == "correct-response":
        prompt.feedback = True
        db.session.commit()
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('dashboard.dashboard'))

@dashboard_blueprint.route('/dashboard/negative/<int:prompt_id>', methods=['POST'])
@login_required
@check_confirmed_mail
def negative_feedback(prompt_id):
    ''' handles user feedback per prompt '''
    prompt = Prompt.query.filter_by(id=prompt_id).first()
    if request.form['incorrect-btn'] == "incorrect-response":
        prompt.feedback = False
        db.session.commit()
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('dashboard.dashboard'))

@dashboard_blueprint.route('/favoriten', methods=['GET', 'POST'])
@login_required
@check_confirmed_mail
def favorites():
    """User favorite Excel Formulas"""
    page = request.args.get('page', 1, type=int)
    favorite_formulas = Prompt.query.filter_by(user_id=current_user.id, favorite=True).order_by(Prompt.created_at).paginate(page=page, per_page=9)
    
    if request.method == 'POST' and request.form['filter_value'] == "Alle":
    
        page = request.args.get('page', 1, type=int)
        favorite_formulas = Prompt.query.filter_by(user_id=current_user.id, favorite=True).order_by(Prompt.created_at).paginate(page=page, per_page=9)
    
    elif request.method == 'POST':
        filter_value = request.form['filter_value']
        page = request.args.get('page', 1, type=int)
        favorite_formulas = Prompt.query.filter_by(user_id=current_user.id, favorite=True, 
                                                   provider=filter_value).order_by(Prompt.created_at).paginate(page=page, per_page=9)
        
    return render_template('dashboard/favorites.html', favorite_formulas=favorite_formulas)

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
