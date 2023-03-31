''' Errorhandler routes '''
from flask import Blueprint, render_template

################
#### config ####
################

error_handlers_blueprint = Blueprint('error_handlers', __name__)

################
#### routes ####
################

@error_handlers_blueprint.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@error_handlers_blueprint.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500