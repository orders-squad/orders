# devops-orders [![Build Status](https://travis-ci.org/orders-squad/orders.svg?branch=master)](https://travis-ci.org/orders-squad/orders)  [![codecov](https://codecov.io/gh/orders-squad/orders/branch/master/graph/badge.svg)](https://codecov.io/gh/orders-squad/orders)  [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Orders microservice


## How to run the code

- In shell:
```shell
vagrant up
vagrant ssh
cd /vagrant
python run.py
```

- Then in your browser's address bar type this address:
`localhost:5000`

If everything works fine, you'll get an `HTTP 200` and a pair of braces`[]`(because the database is empty).

## Create a new order
Please first install `httpie`(`brew install httpie`).  
Then in your terminal please type:
```shell
http --json POST :5000/orders price=11.5 prod_id=1 prod_name='bread' status='test' cust_id=9
```

And if everything works fine, the response is like following:
```
HTTP/1.0 201 CREATED
Content-Length: 127
Content-Type: application/json
Date: Mon, 15 Oct 2018 19:36:43 GMT
Location: http://localhost:5000/orders/8
Server: Werkzeug/0.14.1 Python/2.7.12

{
    "created_on": "Mon, 15 Oct 2018 19:36:43 GMT",
    "cust_id": 9,
    "id": 8,
    "price": 11.5,
    "prod_id": 1,
    "prod_name": "bread",
    "status": "test"
}
```

## List all orders
Use this link:
`http://localhost:5000/orders`

## Run unit tests
Note that Travis CI and codecov have already taken care of building and
testing.  
If you prefer to run the test manually, please run:
```shell
nosetests
```

To see code coverage reports, please run:
```shell
coverage report -m
```
