"""
Models for Orders Service(adapted from Professor Rofrano's demo code)

All of the models are stored in this module

Models
------
Pet - A Pet used in the Pet Store

Attributes:
-----------


"""
import logging
from flask_sqlalchemy import SQLAlchemy


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
    prod_id = db.Column(db.Integer)
    prod_name = db.Column(db.String(63))
    cust_id = db.Column(db.Integer)
    price = db.Column(db.Float)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    status = db.Column(db.String(63))

    def __repr__(self):
        # return '<Order %r>' % (self.name)
        return 'Order {0}, {1}'.format(self.prod_name, self.id)

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
        return {"id": self.id,
                "prod_id": self.prod_id,
                "prod_name": self.prod_name,
                "cust_id": self.cust_id,
                "price": self.price,
                "created_on": self.created_on,
                "status": self.status
                }

    def deserialize(self, data):
        try:
            self.prod_name = data['prod_name']
            self.prod_id = data['prod_id']
            self.cust_id = data['cust_id']
            self.price = float(data['price'])
            self.status = data['status']
        except KeyError as error:
            raise DataValidationError('Invalid order: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid order: body of request contained' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
        Order.logger.info('Initializing database')
        Order.app = app
        db.init_app(app)
        app.app_context().push()
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
        return Order.query.filter(Order.prod_name == name)

    @staticmethod
    def find_by_cust_id(cust_id):
        Order.logger.info('Processing customer id query for %s ...', cust_id)
        return Order.query.filter(Order.cust_id == cust_id)