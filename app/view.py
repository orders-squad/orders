from flask import request, jsonify, Blueprint, make_response
from flask_restful import Resource
from flask_restful import Api
import logging
import sys
from sqlalchemy.exc import SQLAlchemyError
from app.models import db, OrderSchema, Order
from app import app
from flask_api import status


orderSchema = OrderSchema()


class OrderListResource(Resource):
    def get(self):
        orders = Order.all()
        result = orderSchema.dump(orders, many=True)
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = orderSchema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            order = Order(request_dict['qty'], request_dict['price'])
            order.save()
            query = Order.get(order.prod_id)
            result = orderSchema.dump(query)
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollbak()
            resp = jsonify({'error': str(e)})
            return resp, status.HTTP_400_BAD_REQUEST


def add_blueprints(app):
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    main_bp = Blueprint('main', __name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    api.add_resource(OrderListResource, '/orders/')


@app.route('/')
def api_root():
    return 'Welcome to Order RESTful API!'


def init_db():
    cur_app = app
    Order.init_db(cur_app)


def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print('Setting up logging...')
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')

