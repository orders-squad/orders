"""
Test cases for Order Model

Test cases can be run with:
    nosetests
    coverage report -m
"""

import unittest
import os
from app import app
from app.models import Order, db
import app.view as service
import logging


db_user = os.getenv('DB_USER', 'flaskrest02')
db_pass = os.getenv('DB_PASS', 'flaskrest02')
db_name = os.getenv('DB_NAME', 'flaskrest02')
db_addr = os.getenv('DB_ADDR', '127.0.0.1')

DATABASE_URI = \
    "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=db_user,
                                                                  DB_PASS=db_pass,
                                                                  DB_ADDR=db_addr,
                                                                  DB_NAME=db_name)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')


class TestOrders(unittest.TestCase):
    """ Test cases for Orders """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        service.initialize_logging(logging.INFO)
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Order.init_db(app)
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_orders(self):
        """ Get all orders """
        orders = Order.all()
        self.assertEqual(orders, [])

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
