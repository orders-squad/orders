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


db_user = os.getenv('DB_USER', 'flaskrest02')
db_pass = os.getenv('DB_PASS', 'flaskrest02')
db_name = os.getenv('DB_NAME', 'flaskrest02')
db_addr = os.getenv('DB_ADDR', '127.0.0.1')

DATABASE_URI = \
    "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=db_user,
                                                                  DB_PASS=db_pass,
                                                                  DB_ADDR=db_addr,
                                                                  DB_NAME=db_name)


class TestOrders(unittest.TestCase):
    """ Test cases for Orders """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass
