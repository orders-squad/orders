from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from app.models import db, OrderSchema, Order
from flask_api import status


orderSchema = OrderSchema()


class OrderListResource(Resource):
    def get(self):
        orders = Order.get_all()
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
