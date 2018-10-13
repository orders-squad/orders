"""
Order API Service Test Suite

Test cases can be run with the following:
    nosetests -v --with-spec --spec-color
    coverage report -m
    codecov --token=$CODECOV_TOKEN
"""

import unittest
import os
import json
import logging
from flask_api import status
from mock import MagicMock, patch

from app.models import Order, db
import app.view as service

db_user = os.getenv('DB_USER', 'flaskrest02')
db_pass = os.getenv('DB_PASS', 'flaskrest02')
db_name = os.getenv('DB_NAME', 'flaskrest02')
db_addr = os.getenv('DB_ADDR', '127.0.0.1')

DATABASE_URI = \
    "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=db_user,
                                                                  DB_PASS=db_pass,
                                                                  DB_ADDR=db_addr,
                                                                  DB_NAME=db_name)


class TestOrderServer(unittest.TestCase):
    """ Order Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        service.app.debug = False
        service.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass
