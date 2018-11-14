"""
Order API Service Test Suite(Adapted from Professor Rofrano's template

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import unittest

import os
import json
import logging
from flask_api import status    # HTTP Status Codes
from mock import MagicMock, patch

from app.models import Order, OrderItem, DataValidationError, db
import app.service as service

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################


class TestOrderServer(unittest.TestCase):
    """ Order Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        service.app.debug = False
        service.initialize_logging(logging.INFO)
        # Set up the test database
        service.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        service.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        items = [{"prod_id": 1,
                  "prod_name": "kindle",
                  "prod_qty": 2,
                  "prod_price": 49.95,
                  "status": "ordered"
                  },
                 {"prod_id": 2,
                  "prod_name": "iphone 6",
                  "prod_qty": 2,
                  "prod_price": 199,
                  "status": "ordered"
                  }
                 ]
        data = {"cust_id": 1, "items": items}
        order1 = Order(cust_id=1)
        for item in items:
            order1.items.append(OrderItem(prod_id=item['prod_id'],
                                          prod_name=item['prod_name'],
                                          prod_qty=item['prod_qty'],
                                          prod_price=item['prod_price'],
                                          status=item['status']))

        order1.save()

        order2 = Order(cust_id=2)
        for item in items:
            order2.items.append(OrderItem(prod_id=item['prod_id'],
                                          prod_name=item['prod_name'],
                                          prod_qty=item['prod_qty'],
                                          prod_price=item['prod_price'],
                                          status=item['status']))

        order2.save()

        self.client = service.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Order micro-service REST API Service')

    def test_get_order_list(self):
        """ Get a list of Orders """
        resp = self.client.get('/orders')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_create_order(self):
        """ Create a new Order """
        items = [{"prod_id": 1,
                  "prod_name": "kindle",
                  "prod_qty": 2,
                  "prod_price": 49.95,
                  "status": "ordered"
                  },
                 {"prod_id": 2,
                  "prod_name": "iphone 6",
                  "prod_qty": 2,
                  "prod_price": 199,
                  "status": "ordered"
                  }
                 ]
        # save the current number of pets for later comparison
        order_count = self.get_order_count()
        # add a new order
        new_order = {"cust_id": 2, "items": items}
        data = json.dumps(new_order)
        resp = self.client.post('/orders',
                                data=data,
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['cust_id'], 2)
        # check that count has gone up and includes customer id 2
        resp = self.client.get('/orders')
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), order_count + 1)
        self.assertIn(new_json, data)

    def test_create_bad_order(self):
        """ Create a bad order """
        bad_order = dict(prod_id=2, cust_id=2, price=19.2, status='refund_approved')
        data = json.dumps(bad_order)
        resp = self.client.post('/orders',
                                data=data,
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order(self):
        """ Update an existing order """
        order = Order.find_by_name('kindle')[0]
        print order.id
        items = [{"prod_id": 1,
                  "prod_name": "kindle",
                  "prod_qty": 4,
                  "prod_price": 49.95,
                  "status": "ordered"
                  },
                 {"prod_id": 2,
                  "prod_name": "iphone 6",
                  "prod_qty": 2,
                  "prod_price": 199,
                  "status": "ordered"
                  }
                 ]
        new_order = {"cust_id": 2, "items": []}
        data = json.dumps(new_order)
        resp = self.client.put('/orders/{}'.format(order.id),
                               data=data,
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        print(new_json)
        self.assertEqual(new_json['cust_id'], 2)

    def test_delete_order(self):
        """ Delete an Order that exists """
        # save the current number of orders for later comparrison
        order_count = self.get_order_count()
        # delete an order
        resp = self.client.delete('/orders/2', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_order_count()
        self.assertEqual(new_count, order_count - 1)

    def test_query_order_list_by_cust_id(self):
        """ Query Orders by customer id """
        resp = self.client.get('/orders',
                               query_string='cust_id=1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['cust_id'], 1)
        
        
    def test_request_refund(self):
        """ Request a refund """
        resp = self.client.put('/orders/1/request-refund')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['status'], 'refund_requested')

    def test_bad_request_refund(self):
        """ Test a bad refund request error from invalid order id """
        order = 11111
        resp = self.client.put('/orders/{}/request-refund'.format(order))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_approve_refund(self):
        """ Approve a refund """
        resp = self.client.put('/orders/1/approve-refund')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['status'], 'refund_approved')

    def test_display_order(self):
        
        # resp = self.client.post('/orders',
        #                        data=data,
        #                        content_type='application/json')
        resp = self.client.get('/orders/2')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['id'], 2)

    def test_display_nonexisting_order(self):
        """ Get a order that doesn't exist """
        resp = self.client.get('/orders/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_approve_refund(self):
        """ Test a bad refund approval error from invalid order id """
        order = 11111
        resp = self.client.put('/orders/{}/approve-refund'.format(order))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_deny_refund(self):
        """ Deny a refund """
        resp = self.client.put('/orders/1/deny-refund')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['status'], 'refund_denied')

    def test_bad_deny_refund(self):
        """ Test a bad refund denial error from invalid order id """
        order = 11111
        resp = self.client.put('/orders/{}/deny-refund'.format(order))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_supported(self):
        """ Send server a method that is not supported by it """
        resp = self.client.patch('/orders')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_missing_content_type(self):
        """ test check content type """
        new_order = dict(prod_id=3, prod_name='cake', cust_id=3, price=5.2, status='refund_approved')
        data = json.dumps(new_order)
        resp = self.client.post('/orders',
                                data=data)
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # @patch('app.service.Order.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = DataValidationError()
    #     resp = self.client.get('/orders', query_string='name=fruit')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # @patch('service.Pet.find_by_name')
    # def test_mock_search_data(self, pet_find_mock):
    #     """ Test showing how to mock data """
    #     pet_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)


######################################################################
# Utility functions
######################################################################

    def get_order_count(self):
        """ save the current number of orders """
        resp = self.client.get('/orders')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
