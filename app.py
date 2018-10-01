import os
import sys
import logging
from flask import Flask, Blueprint
from flask_restful import Api
from models import db, OrderSchema, Order
from view import OrderListResource

# Create Flask application
app = Flask(__name__)

config_filename = 'config'

app.config.from_object(config_filename)

db.init_app(app)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

app.register_blueprint(api_bp, url_prefix='/api')


@app.route('/')
def hello_world():
    return 'Hello World!'


api.add_resource(OrderListResource, '/orders/')


if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
