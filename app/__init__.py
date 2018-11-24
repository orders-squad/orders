"""
Package: app

Package for the application models and services
This module also sets up the logging to be used with gunicorn
"""
import logging
from flask import Flask
import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))


POSTGRES = {
    'DB_NAME': 'flaskrest02',
    'DB_USER': 'flaskrest02',
    'DB_PASS': 'flaskrest02',
    'DB_ADDR': 'localhost:5432',
}

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        # message = "Expected environment variable '{}' not set.".format(name)
        return POSTGRES[name]
        # raise Exception(message)


DB_NAME = get_env_variable('DB_NAME')
DB_USER = get_env_variable('DB_USER')
DB_PASS = get_env_variable('DB_PASS')
DB_ADDR = get_env_variable('DB_ADDR')

# Create Flask application
app = Flask(__name__)
app.config.from_object('config')
# Use Postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=DB_USER,pw=DB_PASS,url=DB_ADDR,db=DB_NAME)


import service
import models

# # Set up logging for production
# print 'Setting up logging for {}...'.format(__name__)
# if __name__ != '__main__':
#     gunicorn_logger = logging.getLogger('gunicorn.error')
#     if gunicorn_logger:
#         app.logger.handlers = gunicorn_logger.handlers
#         app.logger.setLevel(gunicorn_logger.level)
#
# app.logger.info('Logging established')
