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


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


DB_NAME = get_env_variable('DB_NAME')
DB_USER = get_env_variable('DB_USER')
DB_PASS = get_env_variable('DB_PASS')
DB_ADDR = get_env_variable('DB_ADDR')

# Create Flask application
app = Flask(__name__)
app.config.from_object('config')
# Use Postgres
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgres://{user}:{pw}@{url}/{db}'.format(user=DB_USER, pw=DB_PASS, url=DB_ADDR, db=DB_NAME)


import service
import models
