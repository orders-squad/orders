from flask import Flask, Blueprint
from flask_restful import Api
from app.models import db
from app.view import OrderListResource

# Create Flask application
app = Flask(__name__)

config_filename = 'config'

app.config.from_object(config_filename)

db.init_app(app)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

app.register_blueprint(api_bp, url_prefix='/api')

api.add_resource(OrderListResource, '/orders/')
