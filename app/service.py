"""
Order Service(Adapted from Professor Rofrano's template

Paths:
------
GET /orders - Returns a list all of the Pets
GET /orders/{id} - Returns the Pet with a given id number
POST /orders - creates a new Pet record in the database
PUT /orders/{id} - updates a Pet record in the database
DELETE /orders/{id} - deletes a Pet record in the database
"""

import os
import sys
import logging
import simplejson as json
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from flask_restplus import Api, Resource, fields
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import SQLAlchemy
from app.models import Order, OrderItem, DataValidationError
from . import app


######################################################################
# Configure Swagger before initilaizing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Order REST API Service',
          description='This is an order server.',
          doc='/'
          # prefix='/api'
         )

OrderItemFields = api.model('OrderItem', {
    "id": fields.Integer,
    "order_id": fields.Integer,
    "prod_id": fields.Integer,
    "prod_name": fields.String,
    "prod_qty": fields.Integer,
    "prod_price": fields.Float,
    "status": fields.String,
})

# Define the model so that the docs reflect what can be sent
order_model = api.model('Order', {
    'id': fields.Integer(readOnly=True,
                         description='The unique id assigned internally by service'),
    'cust_id': fields.Integer(required=True,
                          description='The customer ID of the Order'),
    'items': fields.List(fields.Nested(OrderItemFields),
                         required=True,
                         description='The items in this order'),
})


######################################################################
# Special Error Handlers
######################################################################
# @api.errorhandler(DataValidationError)
# def request_validation_error(error):
#     """ Handles Value Errors from bad data """
#     message = error.message or str(error)
#     app.logger.info(message)
#     return {'status':400, 'error': 'Bad Request', 'message': message}, 400

# @api.errorhandler(DatabaseConnectionError)
# def database_connection_error(error):
#     """ Handles Database Errors from connection attempts """
#     message = error.message or str(error)
#     app.logger.critical(message)
#     return {'status':500, 'error': 'Server Error', 'message': message}, 500

######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    app.logger.info("healthcheck")
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)


######################################################################
#  PATH: /orders/{id}
######################################################################
@api.route('/orders/<int:order_id>')
@api.param('order_id', 'The order identifier')
class OrderResource(Resource):
    """
    OrderResource class

    Allows the manipulation of a single Order
    GET /order{id} - Returns an Order with the id
    PUT /order{id} - Update an Order with the id
    DELETE /order{id} -  Deletes an Order with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ORDER
    # ------------------------------------------------------------------
    @api.doc('get_order')
    @api.response(404, 'Order not found')
    @api.marshal_with(order_model)
    def get(self, order_id):
        """
        Retrieve a single Order

        This endpoint will return an Order based on it's id
        :param order_id:
        :return:
        """
        app.logger.info('Finding an order with id [{}]'.format(order_id))
        order = Order.find(order_id)

        if order:
            message = order.serialize()
            return_code = status.HTTP_200_OK
        else:
            message = {'error': 'Order with id: %s was not found' % str(order_id)}
            return_code = status.HTTP_404_NOT_FOUND

        return message, return_code

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ORDER
    # ------------------------------------------------------------------
    @api.doc('Update_order')
    @api.response(404, 'Order not found')
    @api.response(400, 'The posted order data was not valid')
    @api.expect(order_model)
    @api.marshal_with(order_model)
    def put(self, order_id):
        """
        Update an Order

        This endpoint will update an Order based the body that is posted
        """
        app.logger.info('Request to Update an Order with id [%s]', order_id)
        check_content_type('application/json')
        order = Order.find(order_id)
        if not order:
            message = {'error': 'Order with id: %s was not found' % str(order_id)}
            # return 404 instead of raising exceptions
            return_code = status.HTTP_404_NOT_FOUND
            return message, return_code

        data = api.payload
        app.logger.info(data)
        message = order.deserialize(data)
        order.id = order_id
        order.save()
        return_code = status.HTTP_200_OK
        return message, return_code

    # ------------------------------------------------------------------
    # DELETE AN ORDER
    # ------------------------------------------------------------------
    @api.doc('delete_orders')
    @api.response(204, 'Order deleted')
    def delete(self, order_id):
        """
        Delete an Order

        This endpoint will delete an Order based the body that is posted
        """
        app.logger.info("Request to Delete a pet with id [%s]", order_id)
        # check_content_type('application/json')
        order = Order.find(order_id)
        if order:
            order.delete()
        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /pets
######################################################################
@api.route('/orders', strict_slashes=False)
class OrderCollection(Resource):
    """ Handles all interactions with collections of Orders """
    ######################################################################
    # LIST ALL ORDERS
    ######################################################################
    @api.doc('list_orders')
    @api.marshal_list_with(order_model)
    def get(self):
        """ Returns all of the Orders """
        app.logger.info('Request to list Orders...')
        orders = []
        cust_id = request.args.get('cust_id')
        name = request.args.get('prod_name')
        if cust_id:
            orders = Order.find_by_cust_id(cust_id)
        elif name:
            orders = Order.find_by_name(name)
        else:
            orders = Order.all()

        results = [order.serialize() for order in orders]
        app.logger.info('[%s] Orders returned', len(results))
        return results, status.HTTP_200_OK

    ######################################################################
    # ADD A NEW ORDER
    ######################################################################
    @api.doc('create_oders')
    @api.expect(order_model)
    @api.response(400, 'The posted data was not valid')
    @api.response(201, 'Order created successfully')
    @api.marshal_with(order_model, code=201)
    def post(self):
        """
        Creates an Order
        This endpoint will create an Order based the data in the body that is posted
        """
        app.logger.info('Request to create an Order')
        check_content_type('application/json')
        order = Order()
        res, is_success = order.deserialize(api.payload)
        if is_success:
            order.save()
            app.logger.info('Order with new id [%s] saved!', order.id)
            message = order.serialize()
            location_url = api.url_for(OrderResource, order_id=order.id, _external=True)
            return order.serialize(), status.HTTP_201_CREATED, {'Location': location_url}
        else:
            return jsonify(res), status.HTTP_400_BAD_REQUEST


######################################################################
#  PATH: /orders/{id}/request-refund
#  REQUEST A REFUND
######################################################################
@api.route('/orders/<int:order_item_id>/request-refund')
@api.param('order_item_id', 'the order item id')
class RequestRefundResource(Resource):
    """ Requests refund action on an Order"""
    @api.doc('request_refund')
    @api.response(404, 'Order item not found')
    def put(self, order_item_id):
        """
        Request a refund of an order

        This endpoint will request a refund of an Order based the id specified in the path
        """
        order_item = Order.find_by_order_item_id(order_item_id)
        app.logger.info('Request to refund an Order item')
        app.logger.info(order_item)
        if not order_item:
            abort(status.HTTP_404_NOT_FOUND, "Order item id '{}' was not found.".format(order_item_id))
        order_item.status = "refund_requested"
        order = Order.find(order_item.order_id)
        order.save()
        Order.logger.info("Order with order item id '%s' set to status '%s'", order_item.id, order_item.status)
        return order_item.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /orders/{id}/approve-refund
#  APPROVE A REFUND
######################################################################
@api.route('/orders/<int:order_item_id>/approve-refund')
@api.param('order_item_id', 'The order item identifier')
class ApproveRefundResource(Resource):
    """ Approve refund """
    @api.doc('approve_refund')
    @api.response(404, 'Order item not found')
    def put(self, order_item_id):
        """
        Approve a refund of an order

        This endpoint will approve a refund of an Order based the id specified in the path
        """

        order_item = Order.find_by_order_item_id(order_item_id)
        Order.logger.info(order_item)
        if not order_item:
            abort(status.HTTP_404_NOT_FOUND, "Order item id [{}] was not found.".format(order_item_id))
        order_item.status = "refund_approved"
        order = Order.find(order_item.order_id)
        order.save()
        Order.logger.info("Order with order item id '%s' set to status '%s'", order_item.id, order_item.status)
        return order_item.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /orders/{id}/deny-refund
#  DENY A REFUND
######################################################################
@api.route('/orders/<int:order_item_id>/deny-refund')
@api.param('order_item_id', 'The order item identifier')
class DenyRefundResource(Resource):
    """ Deny refund """
    @api.doc('deny_refund')
    @api.response(404, 'Order item not found')
    def put(self, order_item_id):
        """
        Deny a refund of an order

        This endpoint will deny a refund of an Order based the id specified in the path
        """

        order_item = Order.find_by_order_item_id(order_item_id)
        Order.logger.info(order_item)
        if not order_item:
            abort(status.HTTP_404_NOT_FOUND, "Order item id '{}' was not found.".format(order_item_id))
        order_item.status = "refund_denied"
        order = Order.find(order_item.order_id)
        order.save()
        Order.logger.info("Order with order item id '%s' set to status '%s'", order_item.id, order_item.status)
        return order_item.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

@app.before_first_request
def init_db():
    """ Initialies the SQLAlchemy app """
    # global app
    Order.init_db(app)


def check_content_type(content_type):
    """ Checks that the media type is correct """
    if 'Content-Type' in request.headers:
        if request.headers['Content-Type'] == content_type:
            return
        app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 'Content-Type must be {}'.format(content_type))


def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
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
