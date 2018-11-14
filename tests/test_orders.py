"""
Test cases for Order Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from app.models import Order, DataValidationError, db
from app import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################


class TestOrders(unittest.TestCase):
    """ Test Cases for Orders """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Order.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_an_order(self):
        """ Create an order and assert that it exists """
        # note that since the data is not committed yet, the model data only resides in RAM but not in
        # database.
        order = Order(prod_id=0, prod_name='bread', cust_id=1, price=8.2, status='refund_not_requested')
        self.assertIsNotNone(order)
        self.assertIsNone(order.id)
        self.assertEqual(order.prod_name, "bread")
        self.assertEqual(order.cust_id, 1)
        self.assertEqual(order.price, 8.2)
        self.assertEqual(order.created_on, order.updated_on)
        self.assertEqual(order.status, 'refund_not_requested')

    def test_add_an_order(self):
        """ Create an order and add it to the database """
        orders = Order.all()
        self.assertEqual(orders, [])
        order = Order(prod_id=1, prod_name='cake', cust_id=1, price=9.2, status='refund_approved')
        self.assertIsNotNone(order)
        self.assertIsNone(order.id)
        order.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(order.id, 1)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

    def test_update_an_order(self):
        """ Update an Order """
        order = Order(prod_id=1, prod_name='cake', cust_id=1, price=9.2, status='refund_approved')
        order.save()
        self.assertEqual(order.id, 1)
        # Change it an save it
        order.cust_id = 2
        order.save()
        self.assertEqual(order.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        orders = Order.all()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].cust_id, 2)

    def test_delete_an_order(self):
        """ Delete an Order """
        order = Order(prod_id=1, prod_name='cake', cust_id=1, price=9.2, status='refund_approved')
        order.save()
        self.assertEqual(len(Order.all()), 1)
        # delete an order and make sure it isn't in the database
        order.delete()
        self.assertEqual(len(Order.all()), 0)

    def test_serialize_an_order(self):
        """ Test serialization of an order """
        order = Order(prod_id=1, prod_name='cake', cust_id=1, price=9.2, status='refund_approved')
        data = order.serialize()
        self.assertIsNotNone(data)
        self.assertIn('id', data)
        self.assertIsNone(data['id'])
        self.assertIn('prod_name', data)
        self.assertEqual(data['prod_name'], "cake")
        self.assertIn('price', data)
        self.assertEqual(data['price'], 9.2)
        self.assertIn('cust_id', data)
        self.assertEqual(data['cust_id'], 1)

    def test_deserialize_an_order(self):
        """ Test deserialization of an order """
        data = {"prod_id": 1, "prod_name": 'cake', "cust_id": 1,
                "price": 9.2, "status": 'refund_approved'}
        order = Order()
        order.deserialize(data)
        self.assertIsNotNone(order)
        self.assertIsNone(order.id)
        self.assertEqual(order.prod_name, "cake")
        self.assertEqual(order.cust_id, 1)
        self.assertEqual(order.price, 9.2)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        order = Order()
        # self.assertRaises(DataValidationError, order.deserialize, data)
        res, is_success = order.deserialize(data)
        self.assertFalse(is_success)

    def test_find_by_order_id(self):
        """ Find an order by order ID """
        Order(prod_id=0, prod_name='bread', cust_id=1, price=8.2, status='refund_not_requested').save()
        cake = Order(prod_id=1, prod_name='cake', cust_id=1, price=9.2, status='refund_approved')
        cake.save()
        order = Order.find(cake.id)
        self.assertIsNotNone(order)
        self.assertEqual(order.id, cake.id)
        self.assertEqual(order.prod_name, "cake")
        self.assertEqual(order.cust_id, 1)

    def test_find_by_cust_id(self):
        """ Find Orders by customer id """
        Order(prod_id=0, prod_name='bread', cust_id=1, price=8.2, status='refund_not_requested').save()
        Order(prod_id=1, prod_name='cake', cust_id=1, price=9.2, status='refund_approved').save()
        orders = Order.find_by_cust_id(1)
        self.assertEqual(orders[0].cust_id, 1)
        self.assertEqual(orders[0].prod_name, "bread")
        self.assertEqual(orders[0].price, 8.2)

    def test_find_by_name(self):
        """ Find a Order by Product Name """
        Order(prod_id=0, prod_name='bread', cust_id=1, price=8.2, status='refund_not_requested').save()
        Order(prod_id=1, prod_name='cake', cust_id=1, price=9.2, status='refund_approved').save()
        orders = Order.find_by_name("bread")
        self.assertEqual(orders[0].cust_id, 1)
        self.assertEqual(orders[0].prod_name, "bread")
        self.assertEqual(orders[0].price, 8.2)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
