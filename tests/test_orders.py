"""
Test cases for Order Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from app.models import Order, OrderItem, DataValidationError, db
from app import app, get_env_variable


DB_NAME = get_env_variable('DB_NAME')
DB_USER = get_env_variable('DB_USER')
DB_PASS = get_env_variable('DB_PASS')
DB_ADDR = get_env_variable('DB_ADDR')

DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=DB_USER,pw=DB_PASS,url=DB_ADDR,db=DB_NAME)

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
        order = Order(cust_id=1)
        for item in items:
            order.items.append(OrderItem(prod_id=item['prod_id'],
                                         prod_name=item['prod_name'],
                                         prod_qty=item['prod_qty'],
                                         prod_price=item['prod_price'],
                                         status=item['status']))

        self.assertIsNotNone(order)
        self.assertIsNone(order.id)
        self.assertEqual(order.cust_id, 1)
        #order_item = (OrderItem(prod_id=item['prod_id'],
        #                        prod_name=item['prod_name'],
        #                        prod_qty=item['prod_qty'],
        #                        prod_price=item['prod_price'],
        #                        status=item['status']))
        self.assertEqual(order.items[1].prod_id, 2)
        self.assertEqual(order.items[1].prod_name, "iphone 6")
        self.assertEqual(order.items[1].prod_qty, 2)

        self.assertEqual(order.items[1].prod_price, 199)
        self.assertEqual(order.items[1].status, "ordered")
        self.assertEqual(order.created_on, order.updated_on)


    def test_add_an_order(self):
        """ Create an order and add it to the database """
        orders = Order.all()
        self.assertEqual(orders, [])
        order = Order(cust_id=1)
        self.assertIsNotNone(order)
        self.assertIsNone(order.id)
        order.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(order.id, 1)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

    def test_update_an_order(self):
        """ Update an Order """
        order = Order(cust_id=1)
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
        order = Order(cust_id=1)
        order.save()
        self.assertEqual(len(Order.all()), 1)
        # delete an order and make sure it isn't in the database
        order.delete()
        self.assertEqual(len(Order.all()), 0)

    def test_serialize_an_order(self):
        """ Test serialization of an order """
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
        order = Order(cust_id=1)
        for item in items:
            order.items.append(OrderItem(prod_id=item['prod_id'],
                                         prod_name=item['prod_name'],
                                         prod_qty=item['prod_qty'],
                                         prod_price=item['prod_price'],
                                         status=item['status']))

        data = order.serialize()
        self.assertIsNotNone(data)
        self.assertIn('id', data)
        self.assertIsNone(data['id'])
        self.assertIn('items', data)
        self.assertEqual(data['items'][0]['prod_name'], "kindle")
        self.assertEqual(data['items'][0]['prod_qty'], 2)
        self.assertIn('cust_id', data)
        self.assertEqual(data['cust_id'], 1)

    def test_deserialize_an_order(self):
        """ Test deserialization of an order """
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
        order = Order()
        order.deserialize(data)
        self.assertIsNotNone(order)
        self.assertIsNone(order.id)
        self.assertEqual(order.items[0].prod_name, "kindle")
        self.assertEqual(order.cust_id, 1)
        self.assertEqual(order.items[0].prod_price, 49.95)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        order = Order()
        # self.assertRaises(DataValidationError, order.deserialize, data)
        res, is_success = order.deserialize(data)
        self.assertFalse(is_success)

    def test_bad_env_variable(self):
        """ Test non-existant env variable """
        with self.assertRaises(Exception) as context:
            get_env_variable("NOTHING")
        self.assertTrue(context.exception)

    def test_find_by_order_id(self):
        """ Find an order by order ID """
        Order(cust_id=1).save()
        cake = Order(cust_id=1)
        cake.save()
        order = Order.find(cake.id)
        self.assertIsNotNone(order)
        self.assertEqual(order.id, cake.id)
        self.assertEqual(order.cust_id, 1)

    def test_find_or_404(self):
        """ Find an order or 404 """
        Order(cust_id=1).save()
        cake = Order(cust_id=1)
        cake.save()
        order = Order.find_or_404(cake.id)
        self.assertEqual(order.id, cake.id)
        self.assertEqual(order.cust_id, 1)

    def test_find_by_cust_id(self):
        """ Find Orders by customer id """
        Order(cust_id=1).save()
        Order(cust_id=1).save()
        orders = Order.find_by_cust_id(1)
        self.assertEqual(orders[0].cust_id, 1)

    def test_find_by_order_item_id(self):
        """ Find by Order Item"""
        """ Find a Order by Product Name """

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
        order = Order(cust_id=1)
        order_item = order.items.append(OrderItem(prod_id=items[0]['prod_id'],
                                         prod_name=items[0]['prod_name'],
                                         prod_qty=items[0]['prod_qty'],
                                         prod_price=items[0]['prod_price'],
                                         status=items[0]['status']))
        order.save()
        print order.items[0].id
        other_order_item = order.find_by_order_item_id(order.items[0].id)

        self.assertIsNotNone(other_order_item)
        self.assertEqual(order.items[0].id, other_order_item.id)

    def test_find_by_name(self):
        """ Find a Order by Product Name """

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
        order = Order(cust_id=1)
        for item in items:
            order.items.append(OrderItem(prod_id=item['prod_id'],
                                         prod_name=item['prod_name'],
                                         prod_qty=item['prod_qty'],
                                         prod_price=item['prod_price'],
                                         status=item['status']))
        order.save()

        orders = Order.find_by_name("iphone 6")
        self.assertEqual(orders[0].cust_id, 1)
        self.assertEqual(orders[0].items[1].prod_id, 2)
        self.assertEqual(orders[0].items[1].prod_price, 199)

    def test_remove_all(self):
        """ Remove all orders """
        Order.remove_all()
        self.assertEqual(len(Order.all()), 0)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
