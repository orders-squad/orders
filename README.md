# devops-orders [![Build Status](https://travis-ci.org/orders-squad/orders.svg?branch=master)](https://travis-ci.org/orders-squad/orders)
[![codecov](https://codecov.io/gh/orders-squad/orders/branch/master/graph/badge.svg)](https://codecov.io/gh/orders-squad/orders)

Orders microservice


## How to run the code

- In shell:
```shell
vagrant up
vagrant ssh
cd /vagrant
python3 run.py
```

- Then in your browser's address bar type this address:
`localhost:5000/api/orders`

If everything works fine, you'll get an `HTTP 200` and a pair of braces`[]`(because the database is empty).

