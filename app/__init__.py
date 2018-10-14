from flask import Flask
# from app.models import Order

#########################################################
# this method create_app is as per the pattern
# suggested in the following link:
# http://flask.pocoo.org/docs/1.0/patterns/appfactories/
#########################################################


def create_app(config_name):
    app_to_create = Flask(__name__)
    app_to_create.config.from_object(config_name)
    # Order.init_db(app_to_create)
    return app_to_create


config_file = 'config'
app = create_app(config_file)
from app.view import add_blueprints
add_blueprints(app)
