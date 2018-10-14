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
        service.initialize_logging(logging.INFO)
        service.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        service.init_db()
        self.app = service.app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        Order(qty=7, price=8.2).save()
        Order(qty=8, price=9.2).save()
        self.client = service.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        """ Test the home page """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_order_list(self):
        """ Get a list of Orders """
        resp = self.client.get('/api/orders/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_create_order(self):
        """ Create a new Order """
        order_count = self.get_order_count()
        request_dict = dict(qty="7", price="10.2")
        data = json.dumps(request_dict)
        resp = self.client.post('/api/orders/',
                                data=data,
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['qty'], 7)
        self.assertEqual(new_json['price'], '10.2')
        empty_dict = dict()
        data = json.dumps(empty_dict)
        resp = self.client.post('/api/orders/',
                                data=data,
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        bad_dict = dict(bad='bad', nonsense='nonsense')
        data = json.dumps(bad_dict)
        resp = self.client.post('/api/orders/',
                                data=data,
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def get_order_count(self):
        """ get the current number of orders """
        resp = self.client.get('/api/orders/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)


if __name__ == '__main__':
    unittest.main()