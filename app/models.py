from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import logging


db = SQLAlchemy()


class Order(db.Model):
    """
    This is the Order class
    """
    logger = logging.getLogger(__name__)
    app = None
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
    def all():
        """ Returns all orders in the database """
        Order.logger.info("Processing all orders")
        return Order.query.all()

    @staticmethod
    def get(order_id):
        return Order.query.get(order_id)

    def __repr__(self):
        return 'Order: id={}, qty={}, price={}'.format(self.prod_id, self.qty, self.price)

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Order.logger.info('Initializing database')
        Order.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables


class OrderSchema(Schema):
    """
    This Schema is for validation
    """
    prod_id = fields.Integer(dump_only=True)
    qty = fields.Integer()
    price = fields.Decimal(as_string=True)

    class Meta:
        ordered = True
