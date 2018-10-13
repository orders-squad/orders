from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import app


db = SQLAlchemy()
ma = Marshmallow(app)


class Order(db.Model):
    """
    This is the Order class
    """
    __tablename__ = 'order'

    prod_id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, server_default='0')
    price = db.Column(db.Numeric, server_default='0.0')

    def save(self):
        if not self.prod_id:
            db.session.add(self)
        db.session.commit()

    def __init__(self, qty=0, price=0.0):
        self.qty = qty
        self.price = price

    @staticmethod
    def get_all():
        return Order.query.all()

    @staticmethod
    def get(order_id):
        return Order.query.get(order_id)

    def __repr__(self):
        return 'Order: id={}, qty={}, price={}'.format(self.prod_id, self.qty, self.price)


class OrderSchema(ma.Schema):
    """
    This Schema is for validation
    """
    prod_id = fields.Integer(dump_only=True)
    qty = fields.Integer()
    price = fields.Decimal(as_string=True)

    class Meta:
        ordered = True
