from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow
# from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


class Order(db.Model):
    """
    This is the Order class
    """
    __tablename__ = 'order'

    prod_id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, server_default='0')
    price = db.Column(db.Integer, server_default='0')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, qty=0, price=0):
        self.qty = qty
        self.price = price

    @staticmethod
    def get_all():
        return Order.query.all()

    def __repr__(self):
        return 'Order: id={}, qty={}, price={}'.format(self.prod_id, self.qty, self.price)


class OrderSchema(ma.Schema):
    """
    This Schema is for validation
    """
    id = fields.Integer(dump_only=True)
    qty = fields.Integer()
    price = fields.Integer()
