''' Errorhandler routes '''
from flask import Blueprint, render_template
from iqsheets_app.core.forms import NewsletterForm
################
#### config ####
################

error_handlers_blueprint = Blueprint('error_handlers', __name__)


################
#### routes ####
################

@error_handlers_blueprint.app_errorhandler(400)
def bad_request(e):
    form_nl = NewsletterForm()
    return render_template('errors/400.html', form_nl=form_nl), 400

@error_handlers_blueprint.app_errorhandler(403)
def page_forbidden(error):
    form_nl = NewsletterForm()
    return render_template('errors/403.html', form_nl=form_nl), 403

@error_handlers_blueprint.app_errorhandler(404)
def page_not_found(error):
    form_nl = NewsletterForm()
    return render_template('errors/404.html', form_nl=form_nl), 404

@error_handlers_blueprint.app_errorhandler(500)
def internal_server_error(e):
    form_nl = NewsletterForm()
    return render_template('errors/500.html', form_nl=form_nl), 500