from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from .models import db, OrderSchema, Order


orderSchema = OrderSchema()


class OrderListResource(Resource):
    def get(self):
        orders = Order.query.all()
        result = orderSchema.dump(orders, many=True).data
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            resp = {'message': 'No input data provided'}
            return resp, 400
        errors = orderSchema.validate(request_dict)
        if errors:
            return errors, 400
        try:
            order = Order(request_dict['qty'], request_dict['price'])
            order.save()
            query = Order.query.get(order.prod_id)
            result = orderSchema.dump(query).data
            return result, 201
        except SQLAlchemyError as e:
            db.session.rollbak()
            resp = jsonify({'error': str(e)})
            return resp, 400
