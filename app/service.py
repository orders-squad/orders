"""
Order Store Service(Adapted from Professor Rofrano's template

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
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from models import Order, DataValidationError

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    return jsonify(name='Order micro-service REST API Service',
                   version='1.0',
                   paths=url_for('list_orders', _external=True)
                  ), status.HTTP_200_OK

######################################################################
# LIST ALL ORDERS
######################################################################
@app.route('/orders', methods=['GET'])
def list_orders():
    """ Returns all of the Orders """
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
    return make_response(jsonify(results), status.HTTP_200_OK)





######################################################################
# ADD A NEW ORDER
######################################################################
@app.route('/orders', methods=['POST'])
def create_orders():
    """
    Creates an Order
    This endpoint will create an Order based the data in the body that is posted
    """
    check_content_type('application/json')
    order = Order()
    order.deserialize(request.get_json())
    order.save()
    message = order.serialize()
    # Warning: since get_orders has not been implemented yet, we
    # use a placeholder to make nosetests happy, which means
    # we need to add the REAL URL after get_orders code is merged
    location_url = url_for('display_order', id=order.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })


######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_orders(order_id):
    """
    Update an Order

    This endpoint will update an Order based the body that is posted
    """
    check_content_type('application/json')
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    order.deserialize(request.get_json())
    order.id = order_id
    order.save()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE AN EXISTING ORDER
######################################################################
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    Delete an Order
    This endpoint will delete an Order based the body that is posted
    """
    check_content_type('application/json')
    order = Order.find(order_id)
    if order:
        order.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

    
######################################################################
# REQUEST A REFUND
######################################################################
@app.route('/orders/<int:order_id>/request-refund', methods=['PUT'])
def request_refund(order_id):
    """
    Request a refund of an order

    This endpoint will request a refund of an Order based the id specified in the path
    """
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    order.id = order_id
    order.status = "refund_requested"
    order.save()
    Order.logger.info("Order with id '%s' set to status '%s'", order.id, order.status)
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# APPROVE A REFUND
######################################################################
@app.route('/orders/<int:order_id>/approve-refund', methods=['PUT'])
def approve_refund(order_id):
    """
    Approve a refund of an order

    This endpoint will approve a refund of an Order based the id specified in the path
    """
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    order.id = order_id
    order.status = "refund_approved"
    order.save()
    Order.logger.info("Order with id '%s' set to status '%s'", order.id, order.status)
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# DENY A REFUND
######################################################################
@app.route('/orders/<int:order_id>/deny-refund', methods=['PUT'])
def deny_refund(order_id):
    """
    Deny a refund of an order

    This endpoint will deny a refund of an Order based the id specified in the path
    """
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    order.id = order_id
    order.status = "refund_denied"
    order.save()
    Order.logger.info("Order with id '%s' set to status '%s'", order.id, order.status)
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# DISPLAY AN ORDER
######################################################################
@app.route('/orders/<int:id>', methods=['GET'])
def display_order(id):
    '''Retrieve an order with specific id'''
    app.logger.info('Finding an order with id [{}]'.format(id))
    order=Order.find(id)
    
    if order:
        message = order.serialize()
        return_code = status.HTTP_200_OK
    else:
        message = {'error' : 'Order with id: %s was not found' % str(id)}
        return_code = status.HTTP_404_NOT_FOUND
    

    return make_response(jsonify(message),return_code)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
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
