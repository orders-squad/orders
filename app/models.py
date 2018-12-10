"""
Models for Orders Service(adapted from Professor Rofrano's demo code)

All of the models are stored in this module

Models
------
Order - An order model used in the Online Shopping System

Attributes:
-----------


"""
import logging
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Order(db.Model):
    """
        Warning: since decimal is not supported by SQLite, we'll
        use float instead of Numeric as a workaround
    """
    logger = logging.getLogger(__name__)
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        # return '<Order %r>' % (self.name)
        return str(self.serialize())

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """
            Warning: since decimal is not supported by SQLite, we'll
            use float as a workaround
        """
        return {
            "id": self.id,
            "cust_id": self.cust_id,
            "created_on": self.created_on,
            "items": [item.serialize() for item in self.items]
            }

    def deserialize(self, data):
        if not isinstance(data, dict):
            return "Invalid order: body of request contained bad or no data", False
        try:
            self.cust_id = data['cust_id']
            for item in data['items']:
                self.items.append(OrderItem(prod_id=item['prod_id'],
                prod_name = item['prod_name'],
                prod_qty = item['prod_qty'],
                prod_price = float(item['prod_price']),
                status = item['status']))
        except KeyError as error:
            return "Invalid order: missing " + error.args[0], False
        return self, True

    @staticmethod
    def init_db(app):
        Order.logger.info('Initializing database')
        Order.app = app
        db.init_app(app)
        # This context is only used by nosetests so we
        # move it to test code
        # app.app_context().push()
        db.create_all()

    @staticmethod
    def all():
        Order.logger.info('Processing all Orders')
        return Order.query.all()

    @staticmethod
    def find(order_id):
        Order.logger.info('Processing lookup for id %s ...', order_id)
        return Order.query.get(order_id)

    @staticmethod
    def find_or_404(order_id):
        Order.logger.info('Processing lookup or 404 for id %s ...', order_id)
        return Order.query.get_or_404(order_id)

    @staticmethod
    def find_by_name(name):
        Order.logger.info('Processing name query for %s ...', name)
        return Order.query.filter(OrderItem.prod_name == name)


    @staticmethod
    def find_by_order_item_id(id):
        Order.logger.info('Processing name query for %s ...', id)
        return OrderItem.query.get(id)

    @staticmethod
    def find_by_cust_id(cust_id):
        Order.logger.info('Processing customer id query for %s ...', cust_id)
        return Order.query.filter(Order.cust_id == cust_id)

    @staticmethod
    def remove_all():
        """ Remove all orders from the database """
        rows_deleted = Order.query.delete()
        # db.session.commit()
        Order.logger.info("Deleted %d rows", rows_deleted)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete='CASCADE'))
    prod_id = db.Column(db.Integer)
    prod_name = db.Column(db.String(63))
    prod_qty = db.Column(db.Integer)
    prod_price = db.Column(db.Float)
    status = db.Column(db.String(63))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def serialize(self):
        """ Serializes an OrderItem into a dictionary """
        return {
            "id": self.id,
            "order_id": self.order_id,
            "prod_id": self.prod_id,
            "prod_name": self.prod_name,
            "prod_qty": self.prod_qty,
            "prod_price": self.prod_price,
            "status": self.status,
            "created_on": json.dumps(self.created_on, cls=DateTimeEncoder),
            "updated_on": json.dumps(self.updated_on, cls=DateTimeEncoder)
        }
